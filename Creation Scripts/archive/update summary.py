import os
import re

# Function to parse book and chapter from file path
def parse_file_path(file_path):
    parts = file_path.split(os.sep)
    if parts[0] == "Scriptures":
        if len(parts) == 3 and parts[1] == "Doctrine and Covenants":
            # Handle Doctrine and Covenants: e.g., "D&C 1.md"
            book = "Doctrine and Covenants"
            chapter = parts[2].split(" ")[1].replace(".md", "")
            return book, chapter
        elif len(parts) == 4:
            # Handle standard books: e.g., "03 Jacob"
            book_folder = parts[2]
            book = re.sub(r"^\d+\s+", "", book_folder)  # Remove leading digits and spaces
            chapter = parts[3].split(" ")[-1].replace(".md", "")
            return book, chapter
    return None, None

# Function to update the file content
def update_chapter_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract front matter (if any)
    front_matter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if front_matter_match:
        front_matter = front_matter_match.group(0)
        remaining_content = content[front_matter_match.end():]
    else:
        front_matter = ""
        remaining_content = content

    # Parse book and chapter
    book, chapter = parse_file_path(file_path)
    if not book or not chapter:
        print(f"Skipping {file_path}: unable to parse book/chapter")
        return

    # Construct the correct embedded link
    if book == "Doctrine and Covenants":
        embedded_link = f"> ![[{book}#Section {chapter}]]\n"
    else:
        embedded_link = f"> ![[{book}#{book} {chapter}]]\n"

    # Replace the "Chapter Summary" callout with the embed link
    summary_pattern = re.compile(r"(^>>\[!example\]- Chapter Summary\n(>>.*\n|>\s*\n)*)", re.MULTILINE)
    if summary_pattern.search(remaining_content):
        updated_content = summary_pattern.sub(embedded_link, remaining_content)
    else:
        print(f"No 'Chapter Summary' callout found in {file_path}")
        return

    # Write the updated content back to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(front_matter + updated_content)
    print(f"Updated {file_path} successfully")

# Process all markdown files in the Scriptures directory
for root, dirs, files in os.walk("Scriptures"):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            update_chapter_file(file_path)

print("All chapter files have been processed.")