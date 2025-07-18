import json
import re

# Mapping of volume abbreviations to full names for JSON structure
volume_names = {
    "ot": "Old Testament",
    "nt": "New Testament",
    "bofm": "Book of Mormon",
    "dc-testament": "Doctrine and Covenants",
    "pgp": "Pearl of Great Price"
}

# List of all books in the LDS Standard Works with their details
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

# Blue Letter Bible short codes for OT and NT books
blb_short_codes = {
    "Genesis": "gen",
    "Exodus": "exo",
    "Leviticus": "lev",
    "Numbers": "num",
    "Deuteronomy": "deu",
    "Joshua": "jos",
    "Judges": "jdg",
    "Ruth": "rth",
    "1 Samuel": "1sa",
    "2 Samuel": "2sa",
    "1 Kings": "1ki",
    "2 Kings": "2ki",
    "1 Chronicles": "1ch",
    "2 Chronicles": "2ch",
    "Ezra": "ezr",
    "Nehemiah": "neh",
    "Esther": "est",
    "Job": "job",
    "Psalms": "psa",
    "Proverbs": "pro",
    "Ecclesiastes": "ecc",
    "Song of Solomon": "sng",
    "Isaiah": "isa",
    "Jeremiah": "jer",
    "Lamentations": "lam",
    "Ezekiel": "eze",
    "Daniel": "dan",
    "Hosea": "hos",
    "Joel": "joe",
    "Amos": "amo",
    "Obadiah": "oba",
    "Jonah": "jon",
    "Micah": "mic",
    "Nahum": "nah",
    "Habakkuk": "hab",
    "Zephaniah": "zep",
    "Haggai": "hag",
    "Zechariah": "zec",
    "Malachi": "mal",
    "Matthew": "mat",
    "Mark": "mar",
    "Luke": "luk",
    "John": "jhn",
    "Acts": "act",
    "Romans": "rom",
    "1 Corinthians": "1co",
    "2 Corinthians": "2co",
    "Galatians": "gal",
    "Ephesians": "eph",
    "Philippians": "phl",
    "Colossians": "col",
    "1 Thessalonians": "1th",
    "2 Thessalonians": "2th",
    "1 Timothy": "1ti",
    "2 Timothy": "2ti",
    "Titus": "tit",
    "Philemon": "phm",
    "Hebrews": "heb",
    "James": "jas",
    "1 Peter": "1pe",
    "2 Peter": "2pe",
    "1 John": "1jo",
    "2 John": "2jo",
    "3 John": "3jo",
    "Jude": "jde",
    "Revelation": "rev"
}

# Historical Resources mapping for D&C sections
hr_list = [
    {"nn": "01", "sections": [1]},
    {"nn": "03", "sections": [2]},
    {"nn": "04", "sections": [3,4,5]},
    {"nn": "05", "sections": [6,7,8,9]},
    {"nn": "06", "sections": [10,11]},
    {"nn": "07", "sections": [12,13,14,15,16,17]},
    {"nn": "08", "sections": [18]},
    {"nn": "09", "sections": [19]},
    {"nn": "10", "sections": [20,21,22]},
    {"nn": "11", "sections": [23,24,25,26]},
    {"nn": "12", "sections": [27,28]},
    {"nn": "13", "sections": [29]},
    {"nn": "14", "sections": [30,31,32,33,34,35,36]},
    {"nn": "17", "sections": [37,38,39,40]},
    {"nn": "18", "sections": [41,42,43,44]},
    {"nn": "19", "sections": [45]},
    {"nn": "20", "sections": [46,47,48]},
    {"nn": "21", "sections": [49,50]},
    {"nn": "22", "sections": [51,52,53,54,55,56,57]},
    {"nn": "23", "sections": [58,59]},
    {"nn": "24", "sections": [60,61,62,63]},
    {"nn": "25", "sections": [64,65,66]},
    {"nn": "26", "sections": [67,68,69,70]},
    {"nn": "27", "sections": [71,72,73,74,75]},
    {"nn": "28", "sections": [76]},
    {"nn": "29", "sections": [77,78,79,80]},
    {"nn": "30", "sections": [81,82,83]},
    {"nn": "31", "sections": [84]},
    {"nn": "32", "sections": [85,86,87]},
    {"nn": "33", "sections": [88]},
    {"nn": "34", "sections": [89,90,91,92]},
    {"nn": "35", "sections": [93]},
    {"nn": "36", "sections": [94,95,96,97]},
    {"nn": "37", "sections": [98,99,100,101]},
    {"nn": "38", "sections": [102,103,104,105]},
    {"nn": "39", "sections": [106,107,108]},
    {"nn": "40", "sections": [109,110]},
    {"nn": "41", "sections": [111,112,113,114]},
    {"nn": "42", "sections": [115,116,117,118,119,120]},
    {"nn": "43", "sections": [121,122,123]},
    {"nn": "44", "sections": [124]},
    {"nn": "45", "sections": [125,126,127,128]},
    {"nn": "46", "sections": [129,130,131,132]},
    {"nn": "47", "sections": [133,134]},
    {"nn": "48", "sections": [135,136]},
    {"nn": "49", "sections": [137,138]},
]

# Create section to nn mapping
section_to_nn = {}
for entry in hr_list:
    for sec in entry["sections"]:
        section_to_nn[sec] = entry["nn"]

# Joseph Smith Papers mapping for D&C sections
jsp_mapping = {
    1: ["/paperSummary/revelation-1-november-1831-b-dc-1"],
    2: ["/paperSummary/history-1838-1856-volume-a-1-23-december-1805-30-august-1834?p=5"],
    3: ["/paperSummary/revelation-july-1828-dc-3"],
    4: ["/paperSummary/revelation-february-1829-dc-4"],
    5: ["/paperSummary/revelation-march-1829-dc-5"],
    6: ["/paperSummary/revelation-april-1829-a-dc-6"],
    7: ["/paperSummary/account-of-john-april-1829-c-dc-7"],
    8: ["/paperSummary/revelation-april-1829-b-dc-8"],
    9: ["/paperSummary/revelation-april-1829-d-dc-9"],
    10: ["/paperSummary/revelation-spring-1829-dc-10"],
    11: ["/paperSummary/revelation-may-1829-a-dc-11"],
    12: ["/paperSummary/revelation-may-1829-b-dc-12"],
    13: ["/paperSummary/history-1838-1856-volume-a-1-23-december-1805-30-august-1834?p=23"],
    14: ["/paperSummary/revelation-june-1829-a-dc-14"],
    15: ["/paperSummary/revelation-june-1829-c-dc-15"],
    16: ["/paperSummary/revelation-june-1829-d-dc-16"],
    17: ["/paperSummary/revelation-june-1829-e-dc-17"],
    18: ["/paperSummary/revelation-june-1829-b-dc-18"],
    19: ["/paperSummary/revelation-circa-summer-1829-dc-19"],
    20: ["/paperSummary/articles-and-covenants-circa-april-1830-dc-20"],
    21: ["/paperSummary/revelation-6-april-1830-dc-21"],
    22: ["/paperSummary/revelation-16-april-1830-dc-22"],
    23: [
        "/paperSummary/revelation-april-1830-a-dc-231-2",
        "/paperSummary/revelation-april-1830-d-dc-235",
        "/paperSummary/revelation-april-1830-c-dc-234",
        "/paperSummary/revelation-april-1830-e-dc-236-7",
        "/paperSummary/revelation-april-1830-b-dc-233"
    ],
    24: ["/paperSummary/revelation-july-1830-a-dc-24"],
    25: ["/paperSummary/revelation-july-1830-c-dc-25"],
    26: ["/paperSummary/revelation-july-1830-b-dc-26"],
    27: [
        "/paperSummary/revelation-circa-august-1835-dc-27",
        "/paperSummary/revelation-circa-august-1830-dc-27"
    ],
    28: ["/paperSummary/revelation-september-1830-b-dc-28"],
    29: ["/paperSummary/revelation-september-1830-a-dc-29"],
    30: [
        "/paperSummary/revelation-september-1830-c-dc-301-4",
        "/paperSummary/revelation-september-1830-e-dc-309-11",
        "/paperSummary/revelation-september-1830-d-dc-305-8"
    ],
    31: ["/paperSummary/revelation-september-1830-f-dc-31"],
    32: ["/paperSummary/revelation-october-1830-a-dc-32"],
    33: ["/paperSummary/revelation-october-1830-b-dc-33"],
    34: ["/paperSummary/revelation-4-november-1830-dc-34"],
    35: ["/paperSummary/revelation-7-december-1830-dc-35"],
    36: ["/paperSummary/revelation-9-december-1830-dc-36"],
    37: ["/paperSummary/revelation-30-december-1830-dc-37"],
    38: ["/paperSummary/revelation-2-january-1831-dc-38"],
    39: ["/paperSummary/revelation-5-january-1831-dc-39"],
    40: ["/paperSummary/revelation-6-january-1831-dc-40"],
    41: ["/paperSummary/revelation-4-february-1831-dc-41"],
    42: [
        "/paperSummary/revelation-9-february-1831-dc-421-72",
        "/paperSummary/revelation-23-february-1831-dc-4274-93"
    ],
    43: ["/paperSummary/revelation-february-1831-a-dc-43"],
    44: ["/paperSummary/revelation-february-1831-b-dc-44"],
    45: ["/paperSummary/revelation-circa-7-march-1831-dc-45"],
    46: ["/paperSummary/revelation-circa-8-march-1831-a-dc-46"],
    47: ["/paperSummary/revelation-circa-8-march-1831-b-dc-47"],
    48: ["/paperSummary/revelation-10-march-1831-dc-48"],
    49: ["/paperSummary/revelation-7-may-1831-dc-49"],
    50: ["/paperSummary/revelation-9-may-1831-dc-50"],
    51: ["/paperSummary/revelation-20-may-1831-dc-51"],
    52: ["/paperSummary/revelation-6-june-1831-dc-52"],
    53: ["/paperSummary/revelation-8-june-1831-dc-53"],
    54: ["/paperSummary/revelation-10-june-1831-dc-54"],
    55: ["/paperSummary/revelation-14-june-1831-dc-55"],
    56: ["/paperSummary/revelation-15-june-1831-dc-56"],
    57: ["/paperSummary/revelation-20-july-1831-dc-57"],
    58: ["/paperSummary/revelation-1-august-1831-dc-58"],
    59: ["/paperSummary/revelation-7-august-1831-dc-59"],
    60: ["/paperSummary/revelation-8-august-1831-dc-60"],
    61: ["/paperSummary/revelation-12-august-1831-dc-61"],
    62: ["/paperSummary/revelation-13-august-1831-dc-62"],
    63: ["/paperSummary/revelation-30-august-1831-dc-63"],
    64: ["/paperSummary/revelation-11-september-1831-dc-64"],
    65: ["/paperSummary/revelation-30-october-1831-dc-65"],
    66: ["/paperSummary/revelation-29-october-1831-dc-66"],
    67: ["/paperSummary/revelation-circa-2-november-1831-dc-67"],
    68: [
        "/paperSummary/revelation-1-november-1831-a-dc-68",
        "/paper-summary/revelation-circa-june-1835-dc-68/1"
    ],
    69: ["/paperSummary/revelation-11-november-1831-a-dc-69"],
    70: ["/paperSummary/revelation-12-november-1831-dc-70"],
    71: ["/paperSummary/revelation-1-december-1831-dc-71"],
    72: [
        "/paperSummary/revelation-4-december-1831-a-dc-721-8",
        "/paperSummary/revelation-4-december-1831-c-dc-7224-26",
        "/paperSummary/revelation-4-december-1831-b-dc-729-23"
    ],
    73: ["/paperSummary/revelation-10-january-1832-dc-73"],
    74: ["/paperSummary/explanation-of-scripture-1830-dc-74"],
    75: [
        "/paperSummary/revelation-25-january-1832-b-dc-7523-36",
        "/paperSummary/revelation-25-january-1832-a-dc-751-22"
    ],
    76: ["/paperSummary/vision-16-february-1832-dc-76"],
    77: ["/paperSummary/answers-to-questions-between-circa-4-and-circa-20-march-1832-dc-77"],
    78: ["/paperSummary/revelation-1-march-1832-dc-78"],
    79: ["/paperSummary/revelation-12-march-1832-dc-79"],
    80: ["/paperSummary/revelation-7-march-1832-dc-80"],
    81: ["/paperSummary/revelation-15-march-1832-dc-81"],
    82: ["/paperSummary/revelation-26-april-1832-dc-82"],
    83: ["/paperSummary/revelation-30-april-1832-dc-83"],
    84: ["/paperSummary/revelation-22-23-september-1832-dc-84"],
    85: ["/paperSummary/letter-to-william-w-phelps-27-november-1832"],
    86: ["/paperSummary/revelation-6-december-1832-dc-86"],
    87: ["/paperSummary/revelation-25-december-1832-dc-87"],
    88: [
        "/paperSummary/revelation-27-28-december-1832-dc-881-126",
        "/paperSummary/revelation-3-january-1833-dc-88127-137"
    ],
    89: ["/paperSummary/revelation-27-february-1833-dc-89"],
    90: ["/paperSummary/revelation-8-march-1833-dc-90"],
    91: ["/paperSummary/revelation-9-march-1833-dc-91"],
    92: ["/paperSummary/revelation-15-march-1833-dc-92"],
    93: ["/paperSummary/revelation-6-may-1833-dc-93"],
    94: ["/paperSummary/revelation-2-august-1833-b-dc-94"],
    95: ["/paperSummary/revelation-1-june-1833-dc-95"],
    96: ["/paperSummary/revelation-4-june-1833-dc-96"],
    97: ["/paperSummary/revelation-2-august-1833-a-dc-97"],
    98: ["/paperSummary/revelation-6-august-1833-dc-98"],
    99: ["/paperSummary/revelation-29-august-1832-dc-99"],
    100: ["/paperSummary/revelation-12-october-1833-dc-100"],
    101: ["/paperSummary/revelation-16-17-december-1833-dc-101"],
    102: ["/paperSummary/revised-minutes-18-19-february-1834-dc-102"],
    103: ["/paperSummary/revelation-24-february-1834-dc-103"],
    104: ["/paperSummary/revelation-23-april-1834-dc-104"],
    105: ["/paperSummary/revelation-22-june-1834-dc-105"],
    106: ["/paperSummary/revelation-25-november-1834-dc-106"],
    107: [
        "/paper-summary/instruction-on-priesthood-between-circa-1-march-and-circa-4-may-1835-dc-107",
        "/paperSummary/revelation-11-november-1831-b-dc-107-partial"
    ],
    108: ["/paperSummary/revelation-26-december-1835-dc-108"],
    109: ["/paperSummary/prayer-of-dedication-27-march-1836-dc-109"],
    110: ["/paperSummary/visions-3-april-1836-dc-110"],
    111: ["/paperSummary/revelation-6-august-1836-dc-111"],
    112: ["/paperSummary/revelation-23-july-1837-dc-112"],
    113: [
        "/paperSummary/revelation-march-1838-dc-113",
        "paper-summary/questions-and-answers-between-circa-16-and-circa-29-march-1838-b-dc-1137-10/1"
    ],
    114: ["/paperSummary/revelation-11-april-1838-dc-114"],
    115: ["/paperSummary/revelation-26-april-1838-dc-115"],
    116: ["/paperSummary/journal-march-september-1838?p=30"],
    117: ["/paper-summary/revelation-8-july-1838-e-dc-117"],
    118: ["/paperSummary/revelation-8-july-1838-a-dc-118"],
    119: ["/paperSummary/revelation-8-july-1838-c-dc-119"],
    120: ["/paperSummary/revelation-8-july-1838-d-dc-120"],
    121: ["/paper-summary/letter-to-the-church-and-edward-partridge-20-march-1839/3"],
    122: ["/paper-summary/letter-to-edward-partridge-and-the-church-circa-22-march-1839/3"],
    123: ["/paper-summary/letter-to-edward-partridge-and-the-church-circa-22-march-1839/5"],
    124: ["/paperSummary/revelation-19-january-1841-dc-124"],
    125: ["/paperSummary/revelation-circa-march-1841-dc-125"],
    126: ["/paperSummary/revelation-9july-1841-dc-126"],
    127: ["/paperSummary/journal-december-1841-december-1842?p=66"],
    128: ["/paper-summary/letter-to-the-church-7-september-1842-dc-128"],
    129: ["/paper-summary/instruction-9-february-1843-dc-129-as-reported-by-william-clayton"],
    130: [
        "/paper-summary/instruction-2-april-1843-as-reported-by-william-clayton-dc-130",
        "/paper-summary/instruction-2-april-1843-as-reported-by-willard-richards-dc-130"
    ],
    131: [
        "/paper-summary/discourse-17-may-1843-a",
        "/paper-summary/instruction-16-may-1843",
        "/paper-summary/discourse-17-may-1843-b"
    ],
    132: ["/paper-summary/revelation-12-july-1843-dc-132"],
    133: ["/paperSummary/revelation-3-november-1831-dc-133"],
    134: ["/paper-summary/declaration-on-government-and-law-circa-august-1835-dc-134"],
    135: ["/paperSummary/doctrine-and-covenants-1844?p=446"],
    137: ["/paper-summary/visions-21-january-1836-dc-137"]
}

# Initialize the JSON data structure
json_data = {}

# Process each book in the standard works
for book in standard_works:
    # Get volume abbreviation and full name
    volume = book["volume"]
    volume_name = volume_names[volume]
    
    # Initialize volume list if not already present
    if volume_name not in json_data:
        json_data[volume_name] = []
    
    # Convert book ID to three-digit hexadecimal
    book_id_hex = f"{book['book_id']:03x}"
    
    # Generate book-level URLs
    gl_book_url = f"https://churchofjesuschrist.org/study/scriptures/{volume}/{book['abbr']}?lang=eng"
    sci_book_url = f"https://scriptures.byu.edu/#::c{book_id_hex}"
    
    # Initialize chapter list
    chapter_list = []
    
    # Generate chapter URLs if the book has chapters
    if book["chapters"] > 0:
        for chapter in range(1, book["chapters"] + 1):
            # Convert chapter number to two-digit hexadecimal
            chapter_hex = f"{chapter:02x}"
            
            # Generate chapter-level URLs
            gl_chapter_url = f"https://churchofjesuschrist.org/study/scriptures/{volume}/{book['abbr']}/{chapter}?lang=eng"
            sci_chapter_url = f"https://scriptures.byu.edu/#{book_id_hex}{chapter_hex}::c{book_id_hex}{chapter_hex}"
            
            # Create chapter dictionary with Gospel Library and Scripture Citation Index URLs
            chapter_dict = {
                "number": chapter,
                "url": gl_chapter_url,  # Gospel Library URL
                "sci_url": sci_chapter_url  # Scripture Citation Index URL
            }
            
            # Add Bible Hub, Scripture Toolbox, and Blue Letter Bible URLs for Old Testament and New Testament books
            if volume in ["ot", "nt"]:
                # Bible Hub URL
                bh_book_name = book["name"].lower().replace(" ", "_")
                bh_chapter_url = f"https://biblehub.com/{bh_book_name}/{chapter}.htm"
                chapter_dict["bh_url"] = bh_chapter_url
                
                # Scripture Toolbox URL (Fixed for books starting with numbers)
                st_book_name = book["name"]
                if re.match(r'^\d', st_book_name):  # Check if book name starts with a digit
                    st_book_name = re.sub(r'^(\d)\s', r'\1', st_book_name)  # Remove space after digit
                st_book_name = st_book_name.replace(" ", "_")  # Replace remaining spaces with underscores
                st_chapter_url = f"https://scripturetoolbox.com/html/ic/{st_book_name}/{chapter}.html"
                chapter_dict["st_url"] = st_chapter_url
                
                # Blue Letter Bible URL
                short_code = blb_short_codes[book["name"]]
                blb_chapter_url = f"https://www.blueletterbible.org/kjv/{short_code}/{chapter}/1/ss1/"
                chapter_dict["blb_url"] = blb_chapter_url
            
            # Add Isaiah Explained URL specifically for the book of Isaiah
            if book["name"] == "Isaiah":
                ie_chapter_url = f"https://www.isaiahexplained.com/chapter/{chapter}"
                chapter_dict["ie_url"] = ie_chapter_url
            
            # Add Historical Resources URL for D&C sections
            if volume == "dc-testament" and book["name"] == "Sections":
                if chapter in section_to_nn:
                    nn = section_to_nn[chapter]
                    hr_url = f"https://www.churchofjesuschrist.org/study/history/doctrine-and-covenants-historical-resources-2025/{nn}?lang=eng"
                    chapter_dict["hr_url"] = hr_url

            # Add Joseph Smith Papers URLs for D&C sections
            if volume == "dc-testament" and book["name"] == "Sections":
                if chapter in jsp_mapping:
                    urls = jsp_mapping[chapter]
                    base_jsp = "https://www.josephsmithpapers.org"
                    for i, rel_url in enumerate(urls, 1):
                        if rel_url.startswith('/'):
                            full_url = base_jsp + rel_url
                        else:
                            full_url = base_jsp + '/' + rel_url
                        if len(urls) == 1:
                            chapter_dict["jsp_url_1"] = full_url
                        else:
                            chapter_dict[f"jsp_url_{i}"] = full_url
            
            chapter_list.append(chapter_dict)
    
    # Create book dictionary with all details
    book_data = {
        "name": book["name"],
        "url": gl_book_url,  # Gospel Library URL for the book
        "sci_url": sci_book_url,  # Scripture Citation Index URL for the book
    }
    
    # Add FAIR URL for Book of Mormon books (above chapters)
    if volume == "bofm":
        fair_name = book["name"].replace(" ", "_")
        fair_url = f"https://www.fairlatterdaysaints.org/answers/FAIR_Study_Aids/Book_of_Mormon_Resources_by_chapter_and_verse/{fair_name}"
        book_data["fair_url"] = fair_url
    
    # Add chapters after FAIR URL
    book_data["chapters"] = chapter_list
    
    # Special handling for Official Declarations (no chapters, but add HR URL at book level)
    if volume == "dc-testament" and book["name"] in ["Official Declaration 1", "Official Declaration 2"]:
        hr_url = "https://www.churchofjesuschrist.org/study/history/doctrine-and-covenants-historical-resources-2025/50?lang=eng"
        book_data["hr_url"] = hr_url
    
    # Add book data to the appropriate volume
    json_data[volume_name].append(book_data)

# Write the JSON data to a file
with open('lds_scriptures_urls.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4)

# Confirmation message
print("JSON file 'lds_scriptures_urls.json' has been created successfully with Blue Letter Bible links for OT and NT chapters, FAIR links for BoM books, Historical Resources links for D&C sections, and Joseph Smith Papers links for D&C sections.")