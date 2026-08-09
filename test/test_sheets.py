import os
from dotenv import load_dotenv

load_dotenv()

print("1. Environment loaded")
print("2. Spreadsheet ID loaded:", bool(os.getenv("GOOGLE_SHEET_ID")))

from services.sheets_service import add_row

print("3. sheets_service imported")


test_row = [
    "IIT Hostel Life",
    "7 Things Nobody Tells You About IIT Hostel Life",
    "Hidden hostel experiences",
    "You think you know IIT hostel life? Think again.",
    85,
    "Vlog",
    "Current IIT students",
    "https://www.youtube.com/watch?v=test123",
    "2026-08-09"
]

print("4. About to call add_row()")

response = add_row(test_row)

print("5. add_row() completed")

print("Google Sheet updated successfully!")
print(response)