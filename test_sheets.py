import os
from dotenv import load_dotenv

load_dotenv()

print("1. Environment loaded")
print("2. Spreadsheet ID loaded:", bool(os.getenv("GOOGLE_SHEET_ID")))

from services.sheets_service import add_row

print("3. sheets_service imported")


test_row = [
    "IIT Placement Preparation",
    "How I Prepared for IIT Placements",
    "Practical preparation roadmap",
    "I wish I knew these things before placement season.",
    87.5,
    "https://www.youtube.com/",
    "2026-08-08"
]

print("4. About to call add_row()")

response = add_row(test_row)

print("5. add_row() completed")

print("Google Sheet updated successfully!")
print(response)