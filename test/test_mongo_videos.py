from services.mongo_service import (
    client,
    db,
    save_videos
)


test_videos = [
    {
        "video_id": "TEST123",
        "title": "Test IIT Video",
        "channel": "Test Channel",
        "published_at": "2026-08-09T10:00:00Z",
        "views": 10000,
        "likes": 500,
        "comments": 50,
        "views_per_day": 1000,
        "engagement_rate": 5.5,
        "trend_score": 72.5,
        "url": "https://www.youtube.com/watch?v=TEST123"
    }
]


try:

    saved = save_videos(
        test_videos,
        "student life at IIT Madras"
    )

    print("===== MONGODB VIDEO TEST =====")
    print(f"Videos saved: {saved}")

    document = db["videos"].find_one({
        "video_id": "TEST123"
    })

    print("\nSaved document:")
    print(document)

except Exception as error:

    print("===== MONGODB ERROR =====")
    print(type(error).__name__)
    print(error)

finally:

    client.close()