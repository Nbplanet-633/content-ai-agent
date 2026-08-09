from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.settings import YOUTUBE_API_KEY


def search_niche_videos(
    query,
    region_code="IN",
    max_results=20
):
    try:

        # Create YouTube API service
        youtube = build(
            "youtube",
            "v3",
            developerKey=YOUTUBE_API_KEY
        )

        # --------------------------------------------------
        # 1. Search for videos
        # --------------------------------------------------
        response = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            regionCode=region_code,
            maxResults=max_results
        ).execute()

        search_items = response.get("items", [])

        if not search_items:
            return []

        # --------------------------------------------------
        # 2. Extract video IDs
        # --------------------------------------------------
        video_ids = [
            item["id"]["videoId"]
            for item in search_items
            if item.get("id", {}).get("videoId")
        ]

        if not video_ids:
            return []

        # --------------------------------------------------
        # 3. Get statistics for those videos
        # --------------------------------------------------
        statistics_response = youtube.videos().list(
            part="statistics",
            id=",".join(video_ids)
        ).execute()

        # Create:
        # video_id -> statistics
        statistics_map = {}

        for item in statistics_response.get("items", []):

            statistics_map[item["id"]] = item.get(
                "statistics",
                {}
            )

        # --------------------------------------------------
        # 4. Combine search data + statistics
        # --------------------------------------------------
        videos = []

        for item in search_items:

            video_id = item["id"]["videoId"]

            snippet = item["snippet"]

            statistics = statistics_map.get(
                video_id,
                {}
            )

            videos.append({
                "video_id": video_id,

                "title": snippet["title"],

                "channel": snippet["channelTitle"],

                "published_at": snippet["publishedAt"],

                "views": int(
                    statistics.get(
                        "viewCount",
                        0
                    )
                ),

                "likes": int(
                    statistics.get(
                        "likeCount",
                        0
                    )
                ),

                "comments": int(
                    statistics.get(
                        "commentCount",
                        0
                    )
                ),

                "url": (
                    f"https://www.youtube.com/watch?v="
                    f"{video_id}"
                )
            })

        return videos

    except HttpError as error:

        print("\n===== YOUTUBE HTTP ERROR =====")
        print(error)

        return []

    except Exception as error:

        print("\n===== YOUTUBE API ERROR =====")
        print(type(error).__name__)
        print(error)

        return []