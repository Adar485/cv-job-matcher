from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class JobCreate(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    requirements: Optional[str] = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class JobDetail(BaseModel):
    id: int
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    requirements: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MatchResponse(BaseModel):
    id: int
    job_id: int
    job_title: str
    company: Optional[str] = None
    similarity_score: float
    skill_match_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True