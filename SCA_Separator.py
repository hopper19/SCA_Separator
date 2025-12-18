import re
from collections import defaultdict
from pathlib import Path
import shutil
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas


INPUT_FILE = "SCA_Fall2025.lis"
OUTPUT_DIR = Path(INPUT_FILE.rsplit(".", 1)[0] + "_byInstructor")
# delete the output dir if it exists
if OUTPUT_DIR.exists():
    if OUTPUT_DIR.is_dir():
        shutil.rmtree(OUTPUT_DIR)
    else:
        OUTPUT_DIR.unlink()
OUTPUT_DIR.mkdir(exist_ok=True)

# Match instructor line on a page
INSTRUCTOR_REGEX = re.compile(r"Instructor:\s*([^;]+);")

PAGE_HEIGHT, PAGE_WIDTH  = letter
LEFT_MARGIN = 72
TOP_MARGIN = 72
LINE_HEIGHT = 8
FONT_NAME = "Courier"
FONT_SIZE = 8

with open(INPUT_FILE, "r", errors="ignore") as f:
    text = f.read()

# Split into pages using Form Feed
pages = text.split("\f")

sections = defaultdict(list)
current_instructor = None

for page_num, page in enumerate(pages, start=1):
    match = INSTRUCTOR_REGEX.search(page)
    if match:
        current_instructor = match.group(1).strip()
        sections[current_instructor].append(page)

# Generate PDFs
for instructor, pages in sections.items():
    safe_name = instructor.replace(",", "").replace(" ", "_")
    output_pdf = OUTPUT_DIR / f"{safe_name}.pdf"

    c = canvas.Canvas(str(output_pdf), pagesize=landscape(letter))
    c.setFont(FONT_NAME, FONT_SIZE)

    first_page = True
    for page in pages:
        if not first_page:
            c.showPage()
            c.setFont(FONT_NAME, FONT_SIZE)
        first_page = False
        
        y = PAGE_HEIGHT - TOP_MARGIN

        for line in page.splitlines():
            if y < TOP_MARGIN:
                c.showPage()
                c.setFont(FONT_NAME, FONT_SIZE)
                y = PAGE_HEIGHT - TOP_MARGIN

            c.drawString(LEFT_MARGIN, y, line.rstrip())
            y -= LINE_HEIGHT

    c.save()

print("Done. PDFs created per instructor.")
