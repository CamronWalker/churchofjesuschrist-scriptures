import os
import re
import json
from openai import OpenAI, RateLimitError
import time
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key (retrieve from environment variable for security)
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Function to generate AI summaries using OpenAI
def generate_ai_summaries(book, chapter, verses):
    # Concatenate verses into a single text block
    chapter_text = "\n".join([f"Verse {verse}: {text}" for verse, text in sorted(verses.items(), key=lambda x: int(x[0]))])
    
    # Prompt for three summaries
    prompt = (
        f"Provide three summaries for the chapter '{book} {chapter}' from the scriptures:\n"
        "1. A simple summary as if explaining to a young child (1-2 sentences).\n"
        "2. A normal detailed summary (2-3 sentences) capturing the main events, teachings, and themes.\n"
        "3. A short context summary including speaker, location, audience, etc. (1 sentence).\n"
        "4. Also provide 1-3 of the most important tags that relate to this chapter. All talks should start with #Gospel/ and be separated by a space. Some examples could be #Gospel/Atonement #Gospel/Faith #Gospel/EndureToTheEnd all should be related to doctrine as taught by The Church of Jesus Christ of Latter-day Saints.\n"
        "NOTE: Don't start the summaries with 'In {book} {chapter},' or 'In this chapter' etc. Also, you're able to create wiki style links to other book chapter combos. Limit this to only a couple important links or none at all. [[]] Instructions on how to do this: a. Each Chapter has it's own page that you can link to verses with Obsidian's Header references # b. In Obsidian you can replace what is displayed using the bar syntax like this [[1 Nephi 1#5|1 Nephi 1:5-8]] the intent is to include the range as the display text to the first link in the verse but include the links to the rest of the verses but with no display text so that would make this example [[1 Nephi 1#5|1 Nephi 1:5-8]][[1 Nephi 1#6|]][[1 Nephi 1#7|]][[1 Nephi 1#8|]] c. for sections of D&C use [[D&C 1#5]] not Doctrine and Covenants spelled out. d. Be sure to link to each verse in the range with typical dash for ranges and commas, example: [[D&C 11#11|D&C 11:11–14, 24]][[D&C 11#12|]][[D&C 11#13|]][[D&C 11#14|]][[D&C 11#24|]]\n"
        f"Chapter text:\n{chapter_text}\n\n"
        "Output format:\n"
        "Child Summary: [your child summary here]\n"
        "Normal Summary: [your normal summary here]\n"
        "Context Summary: [your context summary here]\n"
        "Tags: [your tags here]"
    )
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            output = response.choices[0].message.content.strip()
            
            # Better parsing to handle multi-line summaries
            lines = output.split("\n")
            current = None
            child_summary_lines = []
            normal_summary_lines = []
            context_summary_lines = []
            tags_lines = []
            
            for line in lines:
                if line.startswith("Child Summary:"):
                    current = child_summary_lines
                    content = line.split(":", 1)[1].strip() if ":" in line else ""
                    if content:
                        current.append(content)
                elif line.startswith("Normal Summary:"):
                    current = normal_summary_lines
                    content = line.split(":", 1)[1].strip() if ":" in line else ""
                    if content:
                        current.append(content)
                elif line.startswith("Context Summary:"):
                    current = context_summary_lines
                    content = line.split(":", 1)[1].strip() if ":" in line else ""
                    if content:
                        current.append(content)
                elif line.startswith("Tags:"):
                    current = tags_lines
                    content = line.split(":", 1)[1].strip() if ":" in line else ""
                    if content:
                        current.append(content)
                else:
                    if current is not None and line.strip():
                        current.append(line.strip())
            
            child_summary = " ".join(child_summary_lines)
            normal_summary = " ".join(normal_summary_lines)
            context_summary = " ".join(context_summary_lines)
            tags_str = " ".join(tags_lines)
            
            # To mitigate rate limits, add a delay between calls
            time.sleep(0)  # delay; adjust based on your rate limit tier
            
            return child_summary, normal_summary, context_summary, tags_str
        except RateLimitError as e:
            wait_time = 2 ** attempt
            print(f"Rate limit hit for {book} {chapter}: {e}. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error generating summary for {book} {chapter}: {e}")
            return "", "", "", ""
    print(f"Max retries exceeded for {book} {chapter}")
    return "", "", "", ""

# Function to extract book and chapter from file path
def get_book_chapter(file_path):
    filename = os.path.basename(file_path).replace('.md', '')
    parts = file_path.split(os.sep)
    category = parts[1] if len(parts) > 1 else ""
    
    if category == "Doctrine and Covenants":
        if filename.startswith("D&C "):
            book = "Doctrine and Covenants"
            chapter = filename.split(" ")[1]
        elif filename.startswith("Official Declaration "):
            book = filename
            chapter = "1"
        else:
            book = "Unknown"
            chapter = "1"
    else:
        # For other categories, book is all but last part of filename, chapter is last
        filename_parts = filename.split(" ")
        chapter = filename_parts[-1]
        book = " ".join(filename_parts[:-1])
    
    return book, chapter

# Function to parse verses from MD file body
def parse_verses(body_lines):
    verses = {}
    i = 0
    while i < len(body_lines):
        if body_lines[i].startswith("###### "):
            verse_num = body_lines[i][7:].strip()
            if i + 1 < len(body_lines) and not body_lines[i + 1].startswith("######"):
                verse_line = body_lines[i + 1].strip()
                # Expect format: "{verse_num} {text}"
                if verse_line.startswith(verse_num + " "):
                    text = verse_line[len(verse_num) + 1:].strip()
                    verses[verse_num] = text
                i += 1
        i += 1
    return verses

# Function to update MD file with summaries
def update_md_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Find frontmatter boundaries
    if lines[0].strip() != "---":
        print(f"Invalid frontmatter in {file_path}")
        return
    second_dash_index = None
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            second_dash_index = idx
            break
    if second_dash_index is None:
        print(f"No closing frontmatter in {file_path}")
        return
    
    # Parse frontmatter
    fm_content = "".join(lines[1:second_dash_index])
    fm = yaml.safe_load(fm_content) or {}
    
    # Body lines
    body_lines = lines[second_dash_index + 1:]
    
    # Parse verses
    verses = parse_verses(body_lines)
    if not verses:
        print(f"No verses found in {file_path}")
        return
    
    # Get book and chapter
    book, chapter = get_book_chapter(file_path)
    
    # Generate summaries
    child_summary, normal_summary, context_summary, tags_str = generate_ai_summaries(book, chapter, verses)
    
    # Update frontmatter
    fm['child_summary'] = child_summary
    fm['summary'] = normal_summary
    fm['context_summary'] = context_summary
    
    # Replace placeholders in body
    body = ''.join(body_lines)
    body = body.replace('%TAGS%', tags_str)
    body = body.replace('%CONTEXT_SUMMARY%', context_summary)
    body = body.replace('%CHILD_SUMMARY%', child_summary)
    body = body.replace('%NORMAL_SUMMARY%', normal_summary)
    body_lines = body.splitlines(keepends=True)
    
    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(fm, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        f.write("---\n")
        f.writelines(body_lines)

# Traverse the Scriptures folder and update all .md files
def main():
    for root, dirs, files in os.walk("Scriptures"):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                update_md_file(file_path)

if __name__ == "__main__":
    main()

print("Summaries have been added to the scripture files successfully.")