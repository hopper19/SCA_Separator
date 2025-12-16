import re
from collections import defaultdict
from pathlib import Path
import shutil

INPUT_FILE = "SCA_Spring2025.lis"
OUTPUT_DIR = Path("SCA_Spring2025_byInstructor")
# delete the output dir if it exists
if OUTPUT_DIR.exists():
    if OUTPUT_DIR.is_dir():
        shutil.rmtree(OUTPUT_DIR)
    else:
        OUTPUT_DIR.unlink()
OUTPUT_DIR.mkdir(exist_ok=True)

# Match instructor line on a page
INSTRUCTOR_REGEX = re.compile(r"Instructor:\s*([^;]+);")

with open(INPUT_FILE, "r", errors="ignore") as f:
    text = f.read()

# Split into pages using Form Feed
pages = text.split("\f")

instructor_pages = defaultdict(list)
current_instructor = None

for page_num, page in enumerate(pages, start=1):
    match = INSTRUCTOR_REGEX.search(page)
    if match:
        current_instructor = match.group(1).strip()
        instructor_pages[current_instructor].append(page)

# Write output files
for instructor, pages in instructor_pages.items():
    safe_name = instructor.replace(",", "").replace(" ", "_")
    out_path = OUTPUT_DIR / f"{safe_name}.lis"

    with open(out_path, "w") as f:
        f.write("\f".join(pages))

print("Done splitting by instructor.")
