import json
import re
import os

# Function to parse the scriptures text file and build verses data
def parse_scriptures_text(file_path):
    verses_data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Regex to match book chapter:verse text
            match = re.match(r'^(.+)\s(\d+):(\d+)\s+(.+)$', line)
            if match:
                book_name, ch_str, vs_str, text = match.groups()
                ch = int(ch_str)
                vs = int(vs_str)
                book_name = book_name.strip()
                # Normalize book names
                if book_name == "Joseph Smith--Matthew":
                    book_name = "Joseph Smith—Matthew"
                elif book_name == "Joseph Smith--History":
                    book_name = "Joseph Smith—History"
                # Initialize if not present
                if book_name not in verses_data:
                    verses_data[book_name] = [[] for _ in range(200)]  # Arbitrary large number for chapters
                # Append verse
                verses_data[book_name][ch - 1].append({"number": vs, "text": text})
    # Trim empty chapters and sort verses
    for book in verses_data:
        verses_data[book] = [chap for chap in verses_data[book] if chap]
        for chap in verses_data[book]:
            chap.sort(key=lambda v: v["number"])
    return verses_data

standard_works = [
    # Old Testament
    {"name": "Genesis", "abbr": "gen", "chapters": 50, "volume": "ot", "book_id": 101},
    {"name": "Exodus", "abbr": "ex", "chapters": 40, "volume": "ot", "book_id": 102},
    {"name": "Leviticus", "abbr": "lev", "chapters": 27, "volume": "ot", "book_id": 103},
    {"name": "Numbers", "abbr": "num", "chapters": 36, "volume": "ot", "book_id": 104},
    {"name": "Deuteronomy", "abbr": "deut", "chapters": 34, "volume": "ot", "book_id": 105},
    {"name": "Joshua", "abbr": "josh", "chapters": 24, "volume": "ot", "book_id": 106},
    {"name": "Judges", "abbr": "judg", "chapters": 21, "volume": "ot", "book_id": 107},
    {"name": "Ruth", "abbr": "ruth", "chapters": 4, "volume": "ot", "book_id": 108},
    {"name": "1 Samuel", "abbr": "1-sam", "chapters": 31, "volume": "ot", "book_id": 109},
    {"name": "2 Samuel", "abbr": "2-sam", "chapters": 24, "volume": "ot", "book_id": 110},
    {"name": "1 Kings", "abbr": "1-kgs", "chapters": 22, "volume": "ot", "book_id": 111},
    {"name": "2 Kings", "abbr": "2-kgs", "chapters": 25, "volume": "ot", "book_id": 112},
    {"name": "1 Chronicles", "abbr": "1-chr", "chapters": 29, "volume": "ot", "book_id": 113},
    {"name": "2 Chronicles", "abbr": "2-chr", "chapters": 36, "volume": "ot", "book_id": 114},
    {"name": "Ezra", "abbr": "ezra", "chapters": 10, "volume": "ot", "book_id": 115},
    {"name": "Nehemiah", "abbr": "neh", "chapters": 13, "volume": "ot", "book_id": 116},
    {"name": "Esther", "abbr": "esth", "chapters": 10, "volume": "ot", "book_id": 117},
    {"name": "Job", "abbr": "job", "chapters": 42, "volume": "ot", "book_id": 118},
    {"name": "Psalms", "abbr": "ps", "chapters": 150, "volume": "ot", "book_id": 119},
    {"name": "Proverbs", "abbr": "prov", "chapters": 31, "volume": "ot", "book_id": 120},
    {"name": "Ecclesiastes", "abbr": "eccl", "chapters": 12, "volume": "ot", "book_id": 121},
    {"name": "Song of Solomon", "abbr": "song", "chapters": 8, "volume": "ot", "book_id": 122},
    {"name": "Isaiah", "abbr": "isa", "chapters": 66, "volume": "ot", "book_id": 123},
    {"name": "Jeremiah", "abbr": "jer", "chapters": 52, "volume": "ot", "book_id": 124},
    {"name": "Lamentations", "abbr": "lam", "chapters": 5, "volume": "ot", "book_id": 125},
    {"name": "Ezekiel", "abbr": "ezek", "chapters": 48, "volume": "ot", "book_id": 126},
    {"name": "Daniel", "abbr": "dan", "chapters": 12, "volume": "ot", "book_id": 127},
    {"name": "Hosea", "abbr": "hosea", "chapters": 14, "volume": "ot", "book_id": 128},
    {"name": "Joel", "abbr": "joel", "chapters": 3, "volume": "ot", "book_id": 129},
    {"name": "Amos", "abbr": "amos", "chapters": 9, "volume": "ot", "book_id": 130},
    {"name": "Obadiah", "abbr": "obad", "chapters": 1, "volume": "ot", "book_id": 131},
    {"name": "Jonah", "abbr": "jonah", "chapters": 4, "volume": "ot", "book_id": 132},
    {"name": "Micah", "abbr": "micah", "chapters": 7, "volume": "ot", "book_id": 133},
    {"name": "Nahum", "abbr": "nahum", "chapters": 3, "volume": "ot", "book_id": 134},
    {"name": "Habakkuk", "abbr": "hab", "chapters": 3, "volume": "ot", "book_id": 135},
    {"name": "Zephaniah", "abbr": "zeph", "chapters": 3, "volume": "ot", "book_id": 136},
    {"name": "Haggai", "abbr": "hag", "chapters": 2, "volume": "ot", "book_id": 137},
    {"name": "Zechariah", "abbr": "zech", "chapters": 14, "volume": "ot", "book_id": 138},
    {"name": "Malachi", "abbr": "mal", "chapters": 4, "volume": "ot", "book_id": 139},
    
    # New Testament
    {"name": "Matthew", "abbr": "matt", "chapters": 28, "volume": "nt", "book_id": 140},
    {"name": "Mark", "abbr": "mark", "chapters": 16, "volume": "nt", "book_id": 141},
    {"name": "Luke", "abbr": "luke", "chapters": 24, "volume": "nt", "book_id": 142},
    {"name": "John", "abbr": "john", "chapters": 21, "volume": "nt", "book_id": 143},
    {"name": "Acts", "abbr": "acts", "chapters": 28, "volume": "nt", "book_id": 144},
    {"name": "Romans", "abbr": "rom", "chapters": 16, "volume": "nt", "book_id": 145},
    {"name": "1 Corinthians", "abbr": "1-cor", "chapters": 16, "volume": "nt", "book_id": 146},
    {"name": "2 Corinthians", "abbr": "2-cor", "chapters": 13, "volume": "nt", "book_id": 147},
    {"name": "Galatians", "abbr": "gal", "chapters": 6, "volume": "nt", "book_id": 148},
    {"name": "Ephesians", "abbr": "eph", "chapters": 6, "volume": "nt", "book_id": 149},
    {"name": "Philippians", "abbr": "phil", "chapters": 4, "volume": "nt", "book_id": 150},
    {"name": "Colossians", "abbr": "col", "chapters": 4, "volume": "nt", "book_id": 151},
    {"name": "1 Thessalonians", "abbr": "1-thes", "chapters": 5, "volume": "nt", "book_id": 152},
    {"name": "2 Thessalonians", "abbr": "2-thes", "chapters": 3, "volume": "nt", "book_id": 153},
    {"name": "1 Timothy", "abbr": "1-tim", "chapters": 6, "volume": "nt", "book_id": 154},
    {"name": "2 Timothy", "abbr": "2-tim", "chapters": 4, "volume": "nt", "book_id": 155},
    {"name": "Titus", "abbr": "titus", "chapters": 3, "volume": "nt", "book_id": 156},
    {"name": "Philemon", "abbr": "phlm", "chapters": 1, "volume": "nt", "book_id": 157},
    {"name": "Hebrews", "abbr": "heb", "chapters": 13, "volume": "nt", "book_id": 158},
    {"name": "James", "abbr": "james", "chapters": 5, "volume": "nt", "book_id": 159},
    {"name": "1 Peter", "abbr": "1-pet", "chapters": 5, "volume": "nt", "book_id": 160},
    {"name": "2 Peter", "abbr": "2-pet", "chapters": 3, "volume": "nt", "book_id": 161},
    {"name": "1 John", "abbr": "1-jn", "chapters": 5, "volume": "nt", "book_id": 162},
    {"name": "2 John", "abbr": "2-jn", "chapters": 1, "volume": "nt", "book_id": 163},
    {"name": "3 John", "abbr": "3-jn", "chapters": 1, "volume": "nt", "book_id": 164},
    {"name": "Jude", "abbr": "jude", "chapters": 1, "volume": "nt", "book_id": 165},
    {"name": "Revelation", "abbr": "rev", "chapters": 22, "volume": "nt", "book_id": 166},
    
    # Book of Mormon
    {"name": "1 Nephi", "abbr": "1-ne", "chapters": 22, "volume": "bofm", "book_id": 205},
    {"name": "2 Nephi", "abbr": "2-ne", "chapters": 33, "volume": "bofm", "book_id": 206},
    {"name": "Jacob", "abbr": "jacob", "chapters": 7, "volume": "bofm", "book_id": 207},
    {"name": "Enos", "abbr": "enos", "chapters": 1, "volume": "bofm", "book_id": 208},
    {"name": "Jarom", "abbr": "jarom", "chapters": 1, "volume": "bofm", "book_id": 209},
    {"name": "Omni", "abbr": "omni", "chapters": 1, "volume": "bofm", "book_id": 210},
    {"name": "Words of Mormon", "abbr": "w-of-m", "chapters": 1, "volume": "bofm", "book_id": 211},
    {"name": "Mosiah", "abbr": "mosiah", "chapters": 29, "volume": "bofm", "book_id": 212},
    {"name": "Alma", "abbr": "alma", "chapters": 63, "volume": "bofm", "book_id": 213},
    {"name": "Helaman", "abbr": "hel", "chapters": 16, "volume": "bofm", "book_id": 214},
    {"name": "3 Nephi", "abbr": "3-ne", "chapters": 30, "volume": "bofm", "book_id": 215},
    {"name": "4 Nephi", "abbr": "4-ne", "chapters": 1, "volume": "bofm", "book_id": 216},
    {"name": "Mormon", "abbr": "morm", "chapters": 9, "volume": "bofm", "book_id": 217},
    {"name": "Ether", "abbr": "ether", "chapters": 15, "volume": "bofm", "book_id": 218},
    {"name": "Moroni", "abbr": "moro", "chapters": 10, "volume": "bofm", "book_id": 219},
    # Doctrine and Covenants
    {"name": "Introduction", "abbr": "introduction", "chapters": 0, "volume": "dc-testament", "book_id": 301},
    {"name": "Sections", "abbr": "dc", "chapters": 138, "volume": "dc-testament", "book_id": 302},
    {"name": "Official Declaration 1", "abbr": "od-1", "chapters": 0, "volume": "dc-testament", "book_id": 303},
    {"name": "Official Declaration 2", "abbr": "od-2", "chapters": 0, "volume": "dc-testament", "book_id": 304},
    # Pearl of Great Price
    {"name": "Moses", "abbr": "moses", "chapters": 8, "volume": "pgp", "book_id": 401},
    {"name": "Abraham", "abbr": "abr", "chapters": 5, "volume": "pgp", "book_id": 402},
    {"name": "Facsimiles", "abbr": "facsimiles", "chapters": 0, "volume": "pgp", "book_id": 403},
    {"name": "Joseph Smith—Matthew", "abbr": "js-m", "chapters": 1, "volume": "pgp", "book_id": 404},
    {"name": "Joseph Smith—History", "abbr": "js-h", "chapters": 1, "volume": "pgp", "book_id": 405},
    {"name": "Articles of Faith", "abbr": "a-of-f", "chapters": 1, "volume": "pgp", "book_id": 406},
]

# Create a mapping from book name to its details
book_details = {book['name']: book for book in standard_works}

# Function to integrate verses into the URL structure
def integrate_verses(urls_data, verses_data):
    for volume_name, books in urls_data.items():
        for book in books:
            book_name = book["name"]
            details = book_details.get(book_name, {})
            book_abbr = details.get("abbr")
            book_total_chapters = details.get("chapters")
            book_id_val = details.get("book_id")
            book["abbr"] = book_abbr
            book["total_chapters"] = book_total_chapters
            book["book_id"] = book_id_val
            if volume_name == "Doctrine and Covenants" and book_name == "Sections":
                book_verses = verses_data.get("Doctrine and Covenants", [])
            else:
                if book_name not in verses_data or "chapters" not in book:
                    continue
                book_verses = verses_data[book_name]
            chapters = book.get("chapters", [])
            for i, chapter in enumerate(chapters):
                if i < len(book_verses):
                    chapter["verses"] = book_verses[i]
    return urls_data

# Function to split and save into separate files in subfolder
def save_to_files(data):
    subfolder = "lds_scriptures_json"
    os.makedirs(subfolder, exist_ok=True)
    volume_to_file = {
        "Old Testament": "old_testament.json",
        "New Testament": "new_testament.json",
        "Book of Mormon": "book_of_mormon.json",
        "Doctrine and Covenants": "doctrine_and_covenants.json",
        "Pearl of Great Price": "pearl_of_great_price.json"
    }
    for volume_name, file_name in volume_to_file.items():
        if volume_name in data:
            volume_data = {volume_name: data[volume_name]}
            file_path = os.path.join(subfolder, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(volume_data, f, indent=4)
            print(f"Saved {file_path}")

# Main execution
if __name__ == "__main__":
    # File paths
    scriptures_txt = "lds-scriptures.txt"
    urls_json = "lds_scriptures_urls.json"
    
    # Parse verses
    verses_data = parse_scriptures_text(scriptures_txt)
    
    # Load URLs JSON
    with open(urls_json, 'r', encoding='utf-8') as f:
        urls_data = json.load(f)
    
    # Integrate verses and additional fields
    integrated_data = integrate_verses(urls_data, verses_data)
    
    # Save to five files in subfolder
    save_to_files(integrated_data)