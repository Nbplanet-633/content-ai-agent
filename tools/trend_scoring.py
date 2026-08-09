import math
from datetime import datetime, timezone


def calculate_views_per_day(views, published_at):
    """
    Calculate average views received per day.
    """

    if views <= 0:
        return 0.0

    published_time = datetime.fromisoformat(
        published_at.replace("Z", "+00:00")
    )

    current_time = datetime.now(timezone.utc)

    age_in_days = max(
        (current_time - published_time).total_seconds() / 86400,
        1
    )

    return round(
        views / age_in_days,
        2
    )


def calculate_engagement_rate(
    views,
    likes,
    comments
):
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


def calculate_recency_score(published_at):
    """
    Calculate a recency score from 0 to 100.

    Newer videos receive a higher score while older
    videos gradually lose trend strength.
    """

    published_time = datetime.fromisoformat(
        published_at.replace("Z", "+00:00")
    )

    current_time = datetime.now(timezone.utc)

    age_in_days = max(
        (current_time - published_time).total_seconds() / 86400,
        0
    )

    # Exponential decay.
    #
    # ~74% after 30 days
    # ~55% after 60 days
    # ~30% after 120 days
    recency_score = 100 * math.exp(
        -age_in_days / 100
    )

    return round(
        max(0, min(recency_score, 100)),
        2
    )


def calculate_velocity_score(
    views_per_day,
    min_views_per_day,
    max_views_per_day
):
    """
    Normalize views-per-day relative to the videos
    in the current search result.
    """

    if views_per_day <= 0:
        return 0.0

    if max_views_per_day <= min_views_per_day:
        return 100.0

    # Logarithmic normalization prevents a single
    # viral video from completely dominating.
    log_value = math.log10(
        max(views_per_day, 1)
    )

    log_min = math.log10(
        max(min_views_per_day, 1)
    )

    log_max = math.log10(
        max(max_views_per_day, 1)
    )

    score = (
        (log_value - log_min)
        / (log_max - log_min)
    ) * 100

    return round(
        max(0, min(score, 100)),
        2
    )


def calculate_trend_score(
    velocity_score,
    engagement_rate,
    recency_score
):
    """
    Calculate the final trend score from 0 to 100.

    Factors:
    - Views velocity: 45%
    - Engagement: 30%
    - Recency: 25%
    """

    engagement_score = min(
        engagement_rate / 10 * 100,
        100
    )

    score = (
        velocity_score * 0.45
        + engagement_score * 0.30
        + recency_score * 0.25
    )

    return round(
        max(0, min(score, 100)),
        2
    )