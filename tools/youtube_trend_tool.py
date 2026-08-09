import json
import re

from crewai.tools import tool

from tools.youtube_api import search_niche_videos
from services.mongo_service import save_videos

from tools.trend_scoring import (
    calculate_views_per_day,
    calculate_engagement_rate,
    calculate_recency_score,
    calculate_velocity_score,
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
            max_results=20
        )

        print(
            f"\nYouTube returned {len(videos)} candidate videos "
            f"for '{query}'."
        )

        if not videos:

            return json.dumps({
                "status": "no_results",
                "message": (
                    f"No YouTube videos were found for "
                    f"the niche '{query}'."
                )
            })

        # --------------------------------------------------
        # Calculate basic metrics
        # --------------------------------------------------

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

            video["recency_score"] = calculate_recency_score(
                video["published_at"]
            )


        # --------------------------------------------------
        # Calculate velocity range
        # --------------------------------------------------

        views_per_day_values = [
            video["views_per_day"]
            for video in videos
        ]

        min_views_per_day = min(
            views_per_day_values,
            default=0
        )

        max_views_per_day = max(
            views_per_day_values,
            default=0
        )


        # --------------------------------------------------
        # Calculate final trend score
        # --------------------------------------------------

        for video in videos:

            video["velocity_score"] = calculate_velocity_score(
                video["views_per_day"],
                min_views_per_day,
                max_views_per_day
            )

            video["trend_score"] = calculate_trend_score(
                video["velocity_score"],
                video["engagement_rate"],
                video["recency_score"]
            )

        videos.sort(
            key=lambda video: video.get("trend_score", 0),
            reverse=True
        )

        videos = videos[:8]

        save_videos(
            videos,
            query
        )

        return videos

        # return json.dumps({
        #     "status": "success",
        #     "query": query,
        #     "videos": videos
        # })

    except Exception as error:

        return json.dumps({
            "status": "error",
            "message": "Unable to retrieve YouTube trend data.",
            "error": str(error)
        })