import os
import re
import json
from openai import OpenAI, RateLimitError
import time
from dotenv import load_dotenv
import argparse
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key (retrieve from environment variable for security)
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# List of volume files
volumes = [
    "old_testament.json",
    "new_testament.json",
    "book_of_mormon.json",
    "doctrine_and_covenants.json",
    "pearl_of_great_price.json"
]

# Book aliases
book_aliases = {
    "D&C": "Doctrine and Covenants"
}

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
        "4. Also provide 1-3 of the most important tags that relate to this chapter. All tags should start with #Gospel/ and be separated by a space. Some examples could be #Gospel/Atonement #Gospel/Faith #Gospel/EndureToTheEnd all should be related to doctrine as taught by The Church of Jesus Christ of Latter-day Saints.\n"
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
            time.sleep(1)  # delay; adjust based on your rate limit tier
            
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

# Helper to find book in list of books
def find_book(books, book_name):
    for b in books:
        if b["name"].lower() == book_name.lower():
            return b
    return None

# Helper to find chapter in list of chapters
def find_chapter(chapters, chapter_num):
    for c in chapters:
        if str(c["number"]) == chapter_num:
            return c
    return None

# Function to update a specific chapter in the JSON
def update_chapter(data, volume_name, books, book_name, chapter_num, file_path):
    book = find_book(books, book_name)
    if book:
        chapter = find_chapter(book["chapters"], chapter_num)
        if chapter:
            print(f"Processing {book_name} {chapter_num}")
            verses_list = chapter.get("verses", [])
            verses = {str(v["number"]): v["text"] for v in verses_list}
            if verses:
                child, normal, context, tags = generate_ai_summaries(book_name, chapter_num, verses)
                if "ai_resources" not in chapter:
                    chapter["ai_resources"] = {}
                chapter["ai_resources"]["child_summary"] = child
                chapter["ai_resources"]["summary"] = normal
                chapter["ai_resources"]["context_summary"] = context
                chapter["ai_resources"]["tags"] = tags
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                return True
    return False

# Function to update all chapters in a book
def update_book(data, volume_name, books, book_name, file_path):
    book = find_book(books, book_name)
    if book:
        chapters = book["chapters"]
        total_chapters = len(chapters)
        with tqdm(total=total_chapters, desc=f"Processing {book_name}", unit="chapter") as pbar:
            for chapter in chapters:
                chapter_num = str(chapter["number"])
                verses_list = chapter.get("verses", [])
                verses = {str(v["number"]): v["text"] for v in verses_list}
                if verses:
                    child, normal, context, tags = generate_ai_summaries(book_name, chapter_num, verses)
                    if "ai_resources" not in chapter:
                        chapter["ai_resources"] = {}
                    chapter["ai_resources"]["child_summary"] = child
                    chapter["ai_resources"]["summary"] = normal
                    chapter["ai_resources"]["context_summary"] = context
                    chapter["ai_resources"]["tags"] = tags
                pbar.update(1)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    return False

# Function to update all books in a volume
def update_volume(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    volume_name = list(data.keys())[0]
    books = data[volume_name]
    total_chapters = sum(len(book["chapters"]) for book in books)
    with tqdm(total=total_chapters, desc=f"Processing {volume_name}", unit="chapter") as pbar:
        for book in books:
            book_name = book["name"]
            for chapter in book["chapters"]:
                chapter_num = str(chapter["number"])
                verses_list = chapter.get("verses", [])
                verses = {str(v["number"]): v["text"] for v in verses_list}
                if verses:
                    child, normal, context, tags = generate_ai_summaries(book_name, chapter_num, verses)
                    if "ai_resources" not in chapter:
                        chapter["ai_resources"] = {}
                    chapter["ai_resources"]["child_summary"] = child
                    chapter["ai_resources"]["summary"] = normal
                    chapter["ai_resources"]["context_summary"] = context
                    chapter["ai_resources"]["tags"] = tags
                pbar.update(1)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update AI summaries in JSON scripture files.")
    parser.add_argument("-update", required=True, help="Volume file (e.g., new_testament.json), book (e.g., Matthew), or book chapter (e.g., Matthew 5)")
    args = parser.parse_args()

    target = args.update.strip()
    processed = False

    if target.endswith(".json"):
        # Update entire volume
        file_path = os.path.join("lds_scriptures_json", target)
        if os.path.exists(file_path):
            update_volume(file_path)
            processed = True
        else:
            print(f"Volume file {target} not found.")
    else:
        parts = target.split()
        is_chapter_update = len(parts) > 1 and re.match(r'^\d+$', parts[-1])
        if is_chapter_update:
            chapter_num = parts[-1]
            book_input = ' '.join(parts[:-1])
        else:
            book_input = target
            chapter_num = None

        book_name = book_aliases.get(book_input, book_input)

        for vol_file in volumes:
            file_path = os.path.join("lds_scriptures_json", vol_file)
            if not os.path.exists(file_path):
                continue
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            volume_name = list(data.keys())[0]
            books = data[volume_name]

            if chapter_num is not None:
                # Update specific chapter
                if update_chapter(data, volume_name, books, book_name, chapter_num, file_path):
                    processed = True
                    break
            else:
                # Update entire book
                if update_book(data, volume_name, books, book_name, file_path):
                    processed = True
                    break

    if processed:
        print("Summaries have been added to the scripture files successfully.")
    else:
        print("No updates performed.")