from typing import List

from pydantic import BaseModel


class ContentIdea(BaseModel):
    topic: str
    suggested_angle: str
    suggested_title: str
    hook: str
    trend_strength: float
    content_format: str
    target_audience: str
    source_reference: str


class TrendCluster(BaseModel):
    trend: str
    strength: float
    reason: str
    supporting_videos: List[str]


class ContentAnalysis(BaseModel):
    ideas: List[ContentIdea]