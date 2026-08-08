from typing import List

from pydantic import BaseModel


class ContentIdea(BaseModel):
    topic: str
    suggested_angle: str
    suggested_title: str
    hook: str
    trend_strength: float
    source_reference: str


class ContentAnalysis(BaseModel):
    ideas: List[ContentIdea]