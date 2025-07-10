import json

"""
Script to modify the 'blb_url' in the LDS scriptures JSON file by appending '1/ss1/' to each URL.
"""

# Read the JSON file
with open('lds_scriptures_urls.json', 'r') as file:
    data = json.load(file)

count = 0

# Traverse the data
for section_name, section in data.items():
    print(f"Processing section: {section_name}")
    for book in section:
        book_name = book['name']
        for chapter in book.get('chapters', []):
            if 'blb_url' in chapter:
                chapter['blb_url'] += '1/ss1/'
                count += 1

print(f"Total 'blb_url' modified: {count}")

# Write the modified data back to a JSON file
with open('modified_lds_scriptures_urls.json', 'w') as file:
    json.dump(data, file, indent=4)