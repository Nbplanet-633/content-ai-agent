from services.mongo_service import (
    client,
    db,
    save_trend_clusters
)


TEST_NICHE = "student life at IIT Madras"


test_clusters = [
    {
        "trend": "Campus Life",
        "strength": 85,
        "reason": (
            "Multiple videos show strong interest "
            "in campus life and daily student experiences."
        ),
        "supporting_videos": [
            "https://www.youtube.com/watch?v=TEST123",
            "https://www.youtube.com/watch?v=TEST456"
        ]
    },
    {
        "trend": "Hostel Life",
        "strength": 72,
        "reason": (
            "Hostel tours and reviews are attracting "
            "student and aspirant audiences."
        ),
        "supporting_videos": [
            "https://www.youtube.com/watch?v=TEST789"
        ]
    }
]


print("===== MONGODB TREND CLUSTER TEST =====")


try:

    saved = save_trend_clusters(
        TEST_NICHE,
        test_clusters
    )

    print(f"Clusters saved: {saved}")

    documents = list(
        db["trend_clusters"].find({
            "niche": TEST_NICHE
        })
    )

    print(f"Clusters found in MongoDB: {len(documents)}")

    for index, document in enumerate(
        documents,
        start=1
    ):
        print(
            f"\n{index}. {document['trend']}"
        )

        print(
            f"Strength: {document['strength']}"
        )

        print(
            f"Supporting videos: "
            f"{len(document['supporting_videos'])}"
        )


except Exception as error:

    print("\n===== MONGODB ERROR =====")
    print(type(error).__name__)
    print(error)


finally:

    client.close()