import os
import re
import json

# Define the lists of books for each category in their standard order
ot_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Malachi"
]
nt_books = [
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians",
    "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]
bom_books = [
    "1 Nephi", "2 Nephi", "Jacob", "Enos", "Jarom", "Omni", "Words of Mormon", "Mosiah",
    "Alma", "Helaman", "3 Nephi", "4 Nephi", "Mormon", "Ether", "Moroni"
]
pogp_books = [
    "Moses", "Abraham", "Joseph Smith—Matthew", "Joseph Smith—History", "Articles of Faith"
]

# Load the JSON file with hyperlinks
with open("lds_scriptures_urls.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Create a dictionary to map book names (as in JSON) to their chapters' URLs
links_dict = {}
for category, books in json_data.items():
    for book in books:
        book_name = book['name']
        links_dict[book_name] = {}
        for chapter in book['chapters']:
            chapter_num = str(chapter['number'])
            links_dict[book_name][chapter_num] = {
                "gospel_library": chapter['url'],
                "scripture_citation_index": chapter['sci_url']
            }

# Debug: Print available books in links_dict to verify JSON loading
print("Books available in links_dict:", list(links_dict.keys()))

# Initialize a dictionary to hold the verses
books = {}

# Read and parse the input file
with open("lds-scriptures.txt", "r", encoding="utf-8") as f:
    for line in f:
        match = re.match(r"^(.*?)\s(\d+:\d+)\s*(.*)$", line.strip())
        if match:
            book = match.group(1).strip()
            chapter_verse = match.group(2)
            text = match.group(3).strip()
            chapter, verse = chapter_verse.split(":")
            chapter = chapter.strip()
            verse = int(verse.strip())

            if book not in books:
                books[book] = {}
            if chapter not in books[book]:
                books[book][chapter] = {}
            books[book][chapter][verse] = text
        else:
            print(f"Skipping invalid line: {line.strip()}")

# Function to determine the category of a book
def get_category(book):
    if book in ot_books:
        return "Old Testament"
    elif book in nt_books:
        return "New Testament"
    elif book in bom_books:
        return "Book of Mormon"
    elif book == "Doctrine and Covenants" or book.startswith("Official Declaration--"):
        return "Doctrine and Covenants"
    elif book in pogp_books or book.replace("--", "—") in pogp_books:
        return "Pearl of Great Price"
    else:
        print(f"Warning: Unknown book '{book}' encountered.")
        return None

# Function to normalize book names for lookup in links_dict
def normalize_book_name(book):
    if book == "Doctrine and Covenants":
        return "Sections"
    elif book.startswith("Official Declaration--"):
        num = book.split("--")[1]
        return f"Official Declaration {num}"
    else:
        return book.replace("--", "—")  # Replace double hyphens with em dash for books like Joseph Smith—Matthew

# Function to write a chapter file
def write_chapter_file(file_path, book, chapter, verses, links_dict):
    category = get_category(book)
    if category:
        # Define the tag based on the category
        tag = {
            "Old Testament": "Scripture/OT",
            "New Testament": "Scripture/NT",
            "Book of Mormon": "Scripture/BoM",
            "Doctrine and Covenants": "Scripture/DandC",
            "Pearl of Great Price": "Scripture/PoGP"
        }[category]
    else:
        tag = ""

    # Normalize the book name for looking up in links_dict
    book_key = normalize_book_name(book)
    # Debug: Print the book and normalized key to verify
    print(f"Processing book: '{book}', normalized to: '{book_key}', chapter: {chapter}")
    # Retrieve hyperlinks, defaulting to empty strings if not found
    gospel_library = links_dict.get(book_key, {}).get(chapter, {}).get("gospel_library", "")
    citation_index = links_dict.get(book_key, {}).get(chapter, {}).get("scripture_citation_index", "")
    # Debug: Print the retrieved links
    if not gospel_library or not citation_index:
        print(f"No links found for {book_key} chapter {chapter}")

    with open(file_path, "w", encoding="utf-8") as f:
        # Write front matter
        f.write("---\n")
        f.write("publish: true\n")
        f.write("tags:\n")
        f.write("  - no-graph\n")
        f.write("cssclasses:\n")
        f.write("  - scriptures\n")
        f.write("---\n")

        # Write chapter details with hyperlinks
        f.write(">[!Properties]+ Chapter Details\n")
        f.write(f">[Gospel Library]({gospel_library})    |    [Citation Index]({citation_index})\n")
        f.write(">>[!example]- Chapter Summary\n")
        f.write(">> \n")
        f.write("> \n")
        f.write(">\n")

        # Write scripture heading
        if tag:
            f.write(f">#{tag}\n")

        # Write verses in order
        for verse_num in sorted(verses.keys()):
            verse_text = verses[verse_num]
            f.write(f"###### {verse_num}\n")
            f.write(f"{verse_text}\n")

# Create the folder structure and files
for book in books:
    category = get_category(book)
    if not category:
        continue

    category_folder = category
    os.makedirs(category_folder, exist_ok=True)

    if category == "Doctrine and Covenants":
        if book == "Doctrine and Covenants":
            for chapter in books[book]:
                file_name = f"D&C {chapter}.md"
                file_path = os.path.join(category_folder, file_name)
                write_chapter_file(file_path, book, chapter, books[book][chapter], links_dict)
        elif book.startswith("Official Declaration--"):
            num = book.split("--")[1]
            for chapter in books[book]:
                file_name = f"Official Declaration {num}.md"
                file_path = os.path.join(category_folder, file_name)
                write_chapter_file(file_path, book, chapter, books[book][chapter], links_dict)
    else:
        book_list = {
            "Old Testament": ot_books,
            "New Testament": nt_books,
            "Book of Mormon": bom_books,
            "Pearl of Great Price": pogp_books
        }[category]
        # Normalize book name for folder creation if necessary
        book_for_folder = book.replace("—", "--")
        book_index = book_list.index(book_for_folder) + 1 if book_for_folder in book_list else book_list.index(book) + 1
        book_folder = f"{book_index:02d} {book_for_folder}"
        full_book_folder = os.path.join(category_folder, book_folder)
        os.makedirs(full_book_folder, exist_ok=True)

        for chapter in books[book]:
            file_name = f"{book_for_folder} {chapter}.md"
            file_path = os.path.join(full_book_folder, file_name)
            write_chapter_file(file_path, book, chapter, books[book][chapter], links_dict)

print("Scripture files have been generated successfully.")