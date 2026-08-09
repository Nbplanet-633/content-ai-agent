import os


from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv(
    "MONGO_DB_NAME",
    "content_ai_agent"
)


if not MONGO_URI:
    raise ValueError(
        "MONGO_URI is not set in the environment."
    )


client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]


videos_collection = db["videos"]

trend_clusters_collection = db["trend_clusters"]

content_ideas_collection = db["content_ideas"]



def save_videos(videos, niche):
    """
    Save YouTube research videos to MongoDB.
    """

    documents = []

    for video in videos:
        document = {
            "video_id": video.get("video_id"),
            "niche": niche,
            "title": video.get("title"),
            "channel": video.get("channel"),
            "published_at": video.get("published_at"),
            "views": video.get("views"),
            "likes": video.get("likes"),
            "comments": video.get("comments"),
            "views_per_day": video.get("views_per_day"),
            "engagement_rate": video.get("engagement_rate"),
            "trend_score": video.get("trend_score"),
            "url": video.get("url"),
            "created_at": datetime.now(timezone.utc)
        }

        documents.append(document)

    if not documents:
        return 0

    for document in documents:
        videos_collection.update_one(
            {
                "video_id": document["video_id"],
                "niche": document["niche"]
            },
            {
                "$set": document
            },
            upsert=True
        )

    return len(documents)

def save_trend_clusters(niche, trend_clusters):
    """
    Save Researcher trend clusters to MongoDB.
    Update an existing cluster if the same niche and trend
    already exist.
    """

    saved_count = 0

    for cluster in trend_clusters:

        document = {
            "niche": niche,
            "trend": cluster.get("trend"),
            "strength": cluster.get("strength"),
            "reason": cluster.get("reason"),
            "supporting_videos": cluster.get(
                "supporting_videos",
                []
            ),
            "created_at": datetime.now(timezone.utc)
        }

        trend_clusters_collection.update_one(
            {
                "niche": niche,
                "trend": cluster.get("trend")
            },
            {
                "$set": document
            },
            upsert=True
        )

        saved_count += 1

    return saved_count

def save_content_ideas(niche, ideas):
    """
    Save generated content ideas to MongoDB.
    """

    saved_count = 0

    for idea in ideas:

        document = {
            "niche": niche,
            "topic": idea.get("topic"),
            "suggested_title": idea.get("suggested_title"),
            "suggested_angle": idea.get("suggested_angle"),
            "hook": idea.get("hook"),
            "trend_strength": idea.get("trend_strength"),
            "content_format": idea.get("content_format"),
            "target_audience": idea.get("target_audience"),
            "source_reference": idea.get("source_reference"),
            "created_at": datetime.now(timezone.utc)
        }

        content_ideas_collection.update_one(
            {
                "niche": niche,
                "topic": idea.get("topic")
            },
            {
                "$set": document
            },
            upsert=True
        )

        saved_count += 1

    return saved_count