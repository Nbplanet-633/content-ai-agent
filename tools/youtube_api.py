from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.settings import YOUTUBE_API_KEY


def search_niche_videos(
    query,
    region_code="IN",
    max_results=5
):
    try:

        # Create YouTube API service
        youtube = build(
            "youtube",
            "v3",
            developerKey=YOUTUBE_API_KEY
        )

        # Search YouTube
        response = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            regionCode=region_code,
            maxResults=max_results
        ).execute()

        videos = []

        for item in response.get("items", []):

            snippet = item["snippet"]

            videos.append({
                "video_id": item["id"]["videoId"],
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "published_at": snippet["publishedAt"],
                "url": (
                    f"https://www.youtube.com/watch?v="
                    f"{item['id']['videoId']}"
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