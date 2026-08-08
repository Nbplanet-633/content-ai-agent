import os

from dotenv import load_dotenv


load_dotenv()


def get_required_env(name: str) -> str:
    """
    Get a required environment variable.

    Raises a clear error if it is missing.
    """

    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


YOUTUBE_API_KEY = get_required_env(
    "YOUTUBE_API_KEY"
)

GROQ_API_KEY = get_required_env(
    "GROQ_API_KEY"
)

GOOGLE_SHEET_ID = get_required_env(
    "GOOGLE_SHEET_ID"
)