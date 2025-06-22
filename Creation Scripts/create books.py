import os
import json
import re

# Load JSON data
with open("lds_scriptures_urls.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Function to get the display name
def get_display_name(book_name, category):
    if category == "Doctrine and Covenants" and book_name == "Sections":
        return "Doctrine and Covenants"
    return book_name

# Process each category and book
for category, books in json_data.items():
    for index, book in enumerate(books, start=1):
        book_name = book["name"]
        display_name = get_display_name(book_name, category)
        chapters = book["chapters"]

        # Generate aliases
        aliases = [f"{display_name} Index"]
        
        # Optional: Add specific aliases (e.g., for Gospels)
        extra_aliases = {
            # Old Testament
            "Genesis": "First Book of Moses, called Genesis",
            "Exodus": "Second Book of Moses, called Exodus",
            "Leviticus": "Third Book of Moses, called Leviticus",
            "Numbers": "Fourth Book of Moses, called Numbers",
            "Deuteronomy": "Fifth Book of Moses, called Deuteronomy",
            "Joshua": "Book of Joshua",
            "Judges": "Book of Judges",
            "Ruth": "Book of Ruth",
            "1 Samuel": "First Book of Samuel",
            "2 Samuel": "Second Book of Samuel",
            "1 Kings": "First Book of Kings",
            "2 Kings": "Second Book of Kings",
            "1 Chronicles": "First Book of the Chronicles",
            "2 Chronicles": "Second Book of the Chronicles",
            "Ezra": "Book of Ezra",
            "Nehemiah": "Book of Nehemiah",
            "Esther": "Book of Esther",
            "Job": "Book of Job",
            "Psalms": "Book of Psalms",
            "Proverbs": "Book of Proverbs",
            "Ecclesiastes": "Book of Ecclesiastes",
            "Song of Solomon": "Song of Songs, which is Solomon's",
            "Isaiah": "Book of Isaiah",
            "Jeremiah": "Book of Jeremiah",
            "Lamentations": "Lamentations of Jeremiah",
            "Ezekiel": "Book of Ezekiel",
            "Daniel": "Book of Daniel",
            "Hosea": "Book of Hosea",
            "Joel": "Book of Joel",
            "Amos": "Book of Amos",
            "Obadiah": "Book of Obadiah",
            "Jonah": "Book of Jonah",
            "Micah": "Book of Micah",
            "Nahum": "Book of Nahum",
            "Habakkuk": "Book of Habakkuk",
            "Zephaniah": "Book of Zephaniah",
            "Haggai": "Book of Haggai",
            "Zechariah": "Book of Zechariah",
            "Malachi": "Book of Malachi",

            # New Testament
            "Matthew": "Gospel According to Matthew",
            "Mark": "Gospel According to Mark",
            "Luke": "Gospel According to Luke",
            "John": "Gospel According to John",
            "Acts": "Acts of the Apostles",
            "Romans": "Epistle of Paul the Apostle to the Romans",
            "1 Corinthians": "First Epistle of Paul the Apostle to the Corinthians",
            "2 Corinthians": "Second Epistle of Paul the Apostle to the Corinthians",
            "Galatians": "Epistle of Paul the Apostle to the Galatians",
            "Ephesians": "Epistle of Paul the Apostle to the Ephesians",
            "Philippians": "Epistle of Paul the Apostle to the Philippians",
            "Colossians": "Epistle of Paul the Apostle to the Colossians",
            "1 Thessalonians": "First Epistle of Paul the Apostle to the Thessalonians",
            "2 Thessalonians": "Second Epistle of Paul the Apostle to the Thessalonians",
            "1 Timothy": "First Epistle of Paul the Apostle to Timothy",
            "2 Timothy": "Second Epistle of Paul the Apostle to Timothy",
            "Titus": "Epistle of Paul the Apostle to Titus",
            "Philemon": "Epistle of Paul the Apostle to Philemon",
            "Hebrews": "Epistle to the Hebrews",
            "James": "General Epistle of James",
            "1 Peter": "First Epistle General of Peter",
            "2 Peter": "Second Epistle General of Peter",
            "1 John": "First Epistle General of John",
            "2 John": "Second Epistle General of John",
            "3 John": "Third Epistle General of John",
            "Jude": "General Epistle of Jude",
            "Revelation": "Revelation of John the Divine",

            # Book of Mormon
            "1 Nephi": "First Book of Nephi",
            "2 Nephi": "Second Book of Nephi",
            "Jacob": "Book of Jacob",
            "Enos": "Book of Enos",
            "Jarom": "Book of Jarom",
            "Omni": "Book of Omni",
            "Mosiah": "Book of Mosiah",
            "Alma": "Book of Alma",
            "Helaman": "Book of Helaman",
            "3 Nephi": "Third Book of Nephi",
            "4 Nephi": "Fourth Book of Nephi",
            "Mormon": "Book of Mormon",
            "Ether": "Book of Ether",
            "Moroni": "Book of Moroni",

            # Pearl of Great Price
            "Moses": "Book of Moses",
            "Abraham": "Book of Abraham"
        }
        if display_name in extra_aliases:
            aliases.append(extra_aliases[display_name])

        # Determine chapter link prefix
        if len(chapters) > 1:
            if display_name == "Doctrine and Covenants":
                prefix = "D&C"
            else:
                prefix = display_name
        else:
            prefix = None  # Single-chapter books use book name directly

        # Create file path
        if category in ["Book of Mormon", "Old Testament", "New Testament", "Pearl of Great Price"]:
            # For categories with multiple books, use numbered subfolders
            book_folder = f"{index:02d} {book_name}"
            full_folder = os.path.join("Scriptures", category, book_folder)
            file_path = os.path.join(full_folder, f"{display_name}.md")
        elif category == "Doctrine and Covenants":
            # For Doctrine and Covenants, place directly in category folder
            file_path = os.path.join("Scriptures", category, f"{display_name}.md")
        else:
            print(f"Unknown category: {category}")
            continue

        # Ensure the folder exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            # Front matter
            f.write("---\n")
            f.write("publish: true\n")
            f.write("aliases:\n")
            for alias in aliases:
                f.write(f"  - {alias}\n")
            f.write("---\n\n")

            # Chapter headings
            for chapter in chapters:
                chapter_num = chapter["number"]
                if prefix:
                    link = f"[[{prefix} {chapter_num}]]"
                else:
                    link = f"[[{display_name}]]"
                f.write(f"##### {link}\n")
                f.write(f"Chapter {chapter_num} Summary Placeholder\n\n")

print("Book index files have been generated successfully.")