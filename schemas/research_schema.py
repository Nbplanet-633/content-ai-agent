from typing import List

from pydantic import BaseModel


class VideoTrend(BaseModel):
    video_id: str
    title: str
    channel: str
    views: int
    views_per_day: float
    engagement_rate: float
    trend_score: float
    published_at: str
    url: str
    trend_reason: str


class ResearchReport(BaseModel):
    niche: str
    region: str
    trends: List[VideoTrend]