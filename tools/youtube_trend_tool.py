import json
import re

from crewai.tools import tool

from tools.youtube_api import search_niche_videos

from tools.trend_scoring import (
    calculate_views_per_day,
    calculate_engagement_rate,
    calculate_trend_score
)


def normalize_text(text):
    """
    Normalize text into lowercase words.
    """

    return set(
        re.findall(
            r"[a-z0-9]+",
            text.lower()
        )
    )


def is_valid_query(query):
    """
    Check whether the query is an obviously invalid/random string.
    """

    query = query.strip()

    if not query:
        return False

    words = normalize_text(query)

    if not words:
        return False

    # Reject obvious random strings.
    # Only reject a word this long if it looks like
    # an unbroken random string.
    for word in words:

        if len(word) >= 15 and len(words) == 1:
            return False

    return True


@tool("youtube_trend_search")
def youtube_trend_search(query: str) -> str:
    """
    Search YouTube for videos related to a content niche in India.
    """

    try:

        query = query.strip()

        # Only reject obviously invalid queries.
        if not is_valid_query(query):

            return json.dumps({
                "status": "invalid_query",
                "message": (
                    f"The niche '{query}' does not appear "
                    "to be a valid content niche."
                )
            })

        videos = search_niche_videos(
            query=query,
            region_code="IN",
            max_results=5
        )

        if not videos:

            return json.dumps({
                "status": "no_results",
                "message": (
                    f"No YouTube videos were found for "
                    f"the niche '{query}'."
                )
            })

        for video in videos:

            video["views_per_day"] = calculate_views_per_day(
                video["views"],
                video["published_at"]
            )

            video["engagement_rate"] = calculate_engagement_rate(
                video["views"],
                video["likes"],
                video["comments"]
            )

            video["trend_score"] = calculate_trend_score(
                video["views_per_day"],
                video["engagement_rate"],
                video["published_at"]
            )

        videos.sort(
            key=lambda video: video["trend_score"],
            reverse=True
        )

        return json.dumps({
            "status": "success",
            "query": query,
            "videos": videos
        })

    except Exception as error:

        return json.dumps({
            "status": "error",
            "message": "Unable to retrieve YouTube trend data.",
            "error": str(error)
        })