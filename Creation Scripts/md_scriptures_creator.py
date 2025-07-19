import os
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
    "Moses", "Abraham", "Joseph Smith--Matthew", "Joseph Smith--History", "Articles of Faith"
]
dc_books = [
    "Doctrine and Covenants", "Official Declaration 1", "Official Declaration 2"
]

json_files = {
    "Old Testament": "old_testament.json",
    "New Testament": "new_testament.json",
    "Book of Mormon": "book_of_mormon.json",
    "Pearl of Great Price": "pearl_of_great_price.json",
    "Doctrine and Covenants": "doctrine_and_covenants.json"
}

book_orders = {
    "Old Testament": ot_books,
    "New Testament": nt_books,
    "Book of Mormon": bom_books,
    "Pearl of Great Price": pogp_books,
    "Doctrine and Covenants": dc_books
}

tag_map = {
    "Old Testament": "Scripture/OT",
    "New Testament": "Scripture/NT",
    "Book of Mormon": "Scripture/BoM",
    "Doctrine and Covenants": "Scripture/DandC",
    "Pearl of Great Price": "Scripture/PoGP"
}

# Function to clean name for front matter key
def clean_key(name):
    return name.lower().replace(' ', '_').replace('-', '_').replace('--', '_').replace("'", "").replace('(', '').replace(')', '')

# Function to write a chapter file
def write_chapter_file(file_path, book_name, chapter_num, verses, resources_list, category, ai_resources):
    tag = tag_map.get(category, "")

    # Handle AI summaries
    if ai_resources:
        context_summary = ai_resources.get("context_summary", "NA")
        child_summary = ai_resources.get("child_summary", "NA")
        normal_summary = ai_resources.get("summary", "NA")
        tags = ai_resources.get("tags", "")
    else:
        context_summary = "NA"
        child_summary = "NA"
        normal_summary = "NA"
        tags = ""

    with open(file_path, "w", encoding="utf-8") as f:
        # Write front matter
        f.write("---\n")
        f.write("publish: true\n")
        f.write("tags:\n")
        f.write("  - no-graph\n")
        if tag:
            f.write(f"  - {tag}\n")
        f.write("cssclasses:\n")
        f.write("  - scriptures\n")
        # Loop through resources to add to front matter
        for res in resources_list:
            key = clean_key(res["name"]) + "_url"
            f.write(f"{key}: {res['url']}\n")
        f.write("---\n")

        # Write chapter details with hyperlinks
        f.write(">[!Properties]+ Resources\n")
        links = "    |    ".join(f"[{res['name']}]({res['url']})" for res in resources_list)
        f.write(f">{links}\n")

        # Write AI summaries
        f.write(">[!AI]- AI Context\n")
        f.write(f">>{context_summary}\n>\n")
        f.write(">[!AI]- AI Child Summary\n")
        f.write(f">>{child_summary}\n>\n")
        f.write(">[!AI]- AI Summary\n")
        f.write(f">>{normal_summary}\n")
        f.write(f">\n>{tags}\n")

        # Write verses with verse number prepended to the text
        for verse_num in sorted(verses.keys()):
            verse_text = verses[verse_num]
            f.write(f"###### {verse_num}\n")
            f.write(f"{verse_num} {verse_text}\n")

# Process each category
for category, json_filename in json_files.items():
    json_file = os.path.join("lds_scriptures_json", json_filename)
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        books_list = data.get(category, [])  # List of book dicts

    for book_dict in books_list:
        book_name = book_dict["name"]
        if category != "Doctrine and Covenants":
            order_list = book_orders[category]
            try:
                book_index = order_list.index(book_name.replace("--", "—")) + 1
            except ValueError:
                try:
                    book_index = order_list.index(book_name) + 1
                except ValueError:
                    print(f"Warning: Book '{book_name}' not found in order list for {category}.")
                    continue
            book_for_folder = book_name.replace("—", "--")
            full_book_folder = os.path.join("Scriptures", category, f"{book_index:02d} {book_for_folder}")
            os.makedirs(full_book_folder, exist_ok=True)
        else:
            full_book_folder = os.path.join("Scriptures", category)
            os.makedirs(full_book_folder, exist_ok=True)

        for chapter_dict in book_dict["chapters"]:
            chapter_num = chapter_dict["number"]
            verses = {v["number"]: v["text"] for v in chapter_dict["verses"]}
            resources_list = chapter_dict.get("chapter_resources", [])
            ai_resources = chapter_dict.get("ai_resources", None)

            if category == "Doctrine and Covenants":
                if book_name == "Sections":
                    file_name = f"D&C {chapter_num}.md"
                elif "Official Declaration" in book_name:
                    num = book_name.split()[-1]
                    file_name = f"Official Declaration {num}.md"
                else:
                    continue  # Skip if not sections or OD
            else:
                file_name = f"{book_for_folder} {chapter_num}.md"

            file_path = os.path.join(full_book_folder, file_name)
            write_chapter_file(file_path, book_name, chapter_num, verses, resources_list, category, ai_resources)

print("Scripture files have been generated successfully.")