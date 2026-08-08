import os
from datetime import datetime

from dotenv import load_dotenv
from config.settings import GOOGLE_SHEET_ID

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


load_dotenv()


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_sheets_service():
    """
    Authenticate the user and return a Google Sheets API service.
    """

    credentials = None

    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not credentials or not credentials.valid:

        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):
            credentials.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            credentials = flow.run_local_server(
                port=0
            )

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    service = build(
        "sheets",
        "v4",
        credentials=credentials
    )

    return service


def add_row(values):
    """
    Append a single row to the Google Sheet.
    """

    spreadsheet_id = GOOGLE_SHEET_ID

    service = get_sheets_service()

    body = {
        "values": [values]
    }

    response = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range="Content Ideas!A:G",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        )
        .execute()
    )

    return response

def add_content_ideas(ideas):
    """
    Add only new content ideas to Google Sheets.
    Duplicate topics are skipped.
    """

    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")

    service = get_sheets_service()

    existing_topics = get_existing_topics()

    new_rows = []
    skipped_count = 0

    for idea in ideas:

        topic = idea["topic"].strip()
        normalized_topic = topic.lower()

        if normalized_topic in existing_topics:
            skipped_count += 1
            continue

        new_rows.append([
            topic,
            idea["suggested_title"],
            idea["suggested_angle"],
            idea["hook"],
            idea["trend_strength"],
            idea["source_reference"],
            datetime.now().strftime("%Y-%m-%d")
        ])

        # Prevent duplicates within the same AI response.
        existing_topics.add(normalized_topic)

    if not new_rows:
        return {
            "added": 0,
            "skipped": skipped_count
        }

    body = {
        "values": new_rows
    }

    response = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A:G",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        )
        .execute()
    )

    return {
        "added": len(new_rows),
        "skipped": skipped_count,
        "response": response
    }


def get_existing_topics():
    """
    Fetch all existing topics from the Google Sheet.
    """

    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")

    service = get_sheets_service()

    response = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A:A"
        )
        .execute()
    )

    rows = response.get("values", [])

    # Skip the header row.
    if len(rows) <= 1:
        return set()

    return {
        row[0].strip().lower()
        for row in rows[1:]
        if row
    }