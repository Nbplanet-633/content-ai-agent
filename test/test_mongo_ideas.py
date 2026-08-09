from services.mongo_service import (
    client,
    db,
    save_content_ideas
)


TEST_NICHE = "student life at IIT Madras"


test_ideas = [
    {
        "topic": "IIT Hostel Life",
        "suggested_title": (
            "7 Things Nobody Tells You "
            "About IIT Hostel Life"
        ),
        "suggested_angle": "Honest hostel experience",
        "hook": (
            "Think IIT hostel life is just "
            "rooms and studying? Think again."
        ),
        "trend_strength": 82,
        "content_format": "Vlog",
        "target_audience": "IIT students",
        "source_reference": (
            "https://www.youtube.com/watch?v=TEST123"
        )
    },
    {
        "topic": "IIT Campus Life",
        "suggested_title": (
            "A Day in the Life of an IIT "
            "Madras Student"
        ),
        "suggested_angle": "Daily student routine",
        "hook": (
            "Ever wondered what a normal day "
            "inside IIT Madras looks like?"
        ),
        "trend_strength": 88,
        "content_format": "Vlog",
        "target_audience": "JEE aspirants",
        "source_reference": (
            "https://www.youtube.com/watch?v=TEST456"
        )
    }
]


print("===== MONGODB CONTENT IDEAS TEST =====")


try:

    saved = save_content_ideas(
        TEST_NICHE,
        test_ideas
    )

    print(f"Ideas saved: {saved}")

    documents = list(
        db["content_ideas"].find({
            "niche": TEST_NICHE
        })
    )

    print(
        f"Ideas found in MongoDB: "
        f"{len(documents)}"
    )

    for index, document in enumerate(
        documents,
        start=1
    ):
        print(
            f"\n{index}. "
            f"{document['topic']}"
        )

        print(
            f"Title: "
            f"{document['suggested_title']}"
        )

        print(
            f"Format: "
            f"{document['content_format']}"
        )

        print(
            f"Audience: "
            f"{document['target_audience']}"
        )


except Exception as error:

    print("\n===== MONGODB ERROR =====")
    print(type(error).__name__)
    print(error)


finally:

    client.close()