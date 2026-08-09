import json

from tools.youtube_trend_tool import youtube_trend_search
from services.mongo_service import videos_collection


QUERY = "student life at IIT Madras"


print("===== YOUTUBE + MONGODB TEST =====")
print(f"Query: {QUERY}")


try:
    # CrewAI tools are executed using .run()
    result = youtube_trend_search.run(QUERY)

    # The tool may return JSON text.
    if isinstance(result, str):
        result = json.loads(result)

    print(f"\nVideos returned by tool: {len(result)}")

    for index, video in enumerate(result, start=1):
        print(
            f"{index}. "
            f"{video.get('title')} | "
            f"Trend Score: {video.get('trend_score')}"
        )

    mongo_count = videos_collection.count_documents({
        "niche": QUERY
    })

    print(f"\nVideos stored in MongoDB: {mongo_count}")


except Exception as error:

    print("\n===== TEST ERROR =====")
    print(type(error).__name__)
    print(error)