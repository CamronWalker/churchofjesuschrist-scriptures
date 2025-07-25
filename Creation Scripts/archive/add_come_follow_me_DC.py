import json
import os

# Path to the JSON file
file_path = os.path.join('lds_scriptures_json', 'doctrine_and_covenants.json')

# Load the JSON data
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Base URL
base_url = "https://www.churchofjesuschrist.org"

# List of CFM lessons with section ranges, range strings, and paths
# (start, end, range_str, path)
lessons = [
    (1, 1, "1", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/02-doctrine-and-covenants-1?lang=eng"),
    (2, 2, "2", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/04-doctrine-and-covenants-2?lang=eng"),
    (3, 5, "3-5", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/05-doctrine-and-covenants-3-5?lang=eng"),
    (6, 9, "6-9", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/06-doctrine-and-covenants-6-9?lang=eng"),
    (10, 11, "10-11", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/07-doctrine-and-covenants-10-11?lang=eng"),
    (12, 17, "12-17", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/08-doctrine-and-covenants-12-17?lang=eng"),
    (18, 18, "18", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/09-doctrine-and-covenants-18?lang=eng"),
    (19, 19, "19", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/10-doctrine-and-covenants-19?lang=eng"),
    (20, 22, "20-22", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/11-doctrine-and-covenants-20-22?lang=eng"),
    (23, 26, "23-26", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/12-doctrine-and-covenants-23-26?lang=eng"),
    (27, 28, "27-28", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/13-doctrine-and-covenants-27-28?lang=eng"),
    (29, 29, "29", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/14-doctrine-and-covenants-29?lang=eng"),
    (30, 36, "30-36", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/15-doctrine-and-covenants-30-36?lang=eng"),
    (37, 40, "37-40", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/17-doctrine-and-covenants-37-40?lang=eng"),
    (41, 44, "41-44", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/18-doctrine-and-covenants-41-44?lang=eng"),
    (45, 45, "45", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/19-doctrine-and-covenants-45?lang=eng"),
    (46, 48, "46-48", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/20-doctrine-and-covenants-46-48?lang=eng"),
    (49, 50, "49-50", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/21-doctrine-and-covenants-49-50?lang=eng"),
    (51, 57, "51-57", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/22-doctrine-and-covenants-51-57?lang=eng"),
    (58, 59, "58-59", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/23-doctrine-and-covenants-58-59?lang=eng"),
    (60, 63, "60-63", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/24-doctrine-and-covenants-60-63?lang=eng"),
    (64, 66, "64-66", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/25-doctrine-and-covenants-64-66?lang=eng"),
    (67, 70, "67-70", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/26-doctrine-and-covenants-67-70?lang=eng"),
    (71, 75, "71-75", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/27-doctrine-and-covenants-71-75?lang=eng"),
    (76, 76, "76", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/28-doctrine-and-covenants-76?lang=eng"),
    (77, 80, "77-80", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/29-doctrine-and-covenants-77-80?lang=eng"),
    (81, 83, "81-83", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/30-doctrine-and-covenants-81-83?lang=eng"),
    (84, 84, "84", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/31-doctrine-and-covenants-84?lang=eng"),
    (85, 87, "85-87", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/32-doctrine-and-covenants-85-87?lang=eng"),
    (88, 88, "88", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/33-doctrine-and-covenants-88?lang=eng"),
    (89, 92, "89-92", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/34-doctrine-and-covenants-89-92?lang=eng"),
    (93, 93, "93", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/35-doctrine-and-covenants-93?lang=eng"),
    (94, 97, "94-97", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/36-doctrine-and-covenants-94-97?lang=eng"),
    (98, 101, "98-101", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/37-doctrine-and-covenants-98-101?lang=eng"),
    (102, 105, "102-105", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/38-doctrine-and-covenants-102-105?lang=eng"),
    (106, 108, "106-108", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/39-doctrine-and-covenants-106-108?lang=eng"),
    (109, 110, "109-110", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/40-doctrine-and-covenants-109-110?lang=eng"),
    (111, 114, "111-114", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/41-doctrine-and-covenants-111-114?lang=eng"),
    (115, 120, "115-120", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/42-doctrine-and-covenants-115-120?lang=eng"),
    (121, 123, "121-123", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/43-doctrine-and-covenants-121-123?lang=eng"),
    (124, 124, "124", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/44-doctrine-and-covenants-124?lang=eng"),
    (125, 128, "125-128", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/45-doctrine-and-covenants-125-128?lang=eng"),
    (129, 132, "129-132", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/46-doctrine-and-covenants-129-132?lang=eng"),
    (133, 134, "133-134", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/47-doctrine-and-covenants-133-134?lang=eng"),
    (135, 136, "135-136", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/48-doctrine-and-covenants-135-136?lang=eng"),
    (137, 138, "137-138", "/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/49-doctrine-and-covenants-137-138?lang=eng")
]

# Create a mapping from section number to resource dict
section_to_resource = {}
for start, end, range_str, path in lessons:
    url = base_url + path
    name = f"CFM 2025 (Ch {range_str})"
    for sec in range(start, end + 1):
        section_to_resource[sec] = {"name": name, "url": url}

# Update each chapter
for chapter in data['Doctrine and Covenants'][1]['chapters']:
    num = chapter['number']
    if num in section_to_resource:
        new_res = section_to_resource[num]
        if 'chapter_resources' not in chapter:
            chapter['chapter_resources'] = []
        # Check for duplicate by URL
        existing_urls = [res['url'] for res in chapter['chapter_resources']]
        if new_res['url'] not in existing_urls:
            chapter['chapter_resources'].append(new_res)

# Save the updated JSON
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)