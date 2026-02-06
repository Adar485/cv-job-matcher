from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any


class CVCreate(BaseModel):
    file_name: str


class SkillInfo(BaseModel):
    name: str
    confidence_score: float

    class Config:
        from_attributes = True


class CVResponse(BaseModel):
    id: int
    file_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CVDetail(BaseModel):
    id: int
    file_name: Optional[str] = None
    raw_text: Optional[str] = None
    parsed_data: Optional[Any] = None
    skills: List[SkillInfo] = []
    created_at: datetime

    class Config:
        from_attributes = True