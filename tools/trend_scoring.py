import math
from datetime import datetime, timezone


def calculate_views_per_day(views, published_at):
    """
    Calculate average views received per day.
    """

    published_time = datetime.fromisoformat(
        published_at.replace("Z", "+00:00")
    )

    current_time = datetime.now(timezone.utc)

    age_in_days = max(
        (current_time - published_time).total_seconds() / 86400,
        1
    )

    return round(views / age_in_days, 2)


def calculate_engagement_rate(views, likes, comments):
    """
    Calculate engagement rate using likes and comments.
    """

    if views <= 0:
        return 0.0

    engagement = likes + comments

    return round(
        (engagement / views) * 100,
        4
    )


def calculate_trend_score(
    views_per_day,
    engagement_rate,
    published_at
):
    """
    Calculate a trend score from 0 to 100.

    Factors:
    - Views velocity: 50%
    - Engagement: 30%
    - Recency: 20%
    """

    published_time = datetime.fromisoformat(
        published_at.replace("Z", "+00:00")
    )

    current_time = datetime.now(timezone.utc)

    age_in_days = max(
        (current_time - published_time).total_seconds() / 86400,
        1
    )

    # Logarithmic scaling prevents extremely viral
    # videos from dominating the score.
    velocity_score = min(
        math.log10(max(views_per_day, 1)) / 6 * 100,
        100
    )

    engagement_score = min(
        engagement_rate / 10 * 100,
        100
    )

    # Newer videos receive a higher recency score.
    recency_score = max(
        0,
        100 - (age_in_days * 3)
    )

    score = (
        velocity_score * 0.5
        + engagement_score * 0.3
        + recency_score * 0.2
    )

    return round(
        min(score, 100),
        2
    )