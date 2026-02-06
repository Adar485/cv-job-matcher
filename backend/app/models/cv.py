from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String(500))
    file_name = Column(String(255))
    raw_text = Column(Text)
    parsed_data = Column(JSON)
    embedding = Column(JSON)  # BERT embedding vektörü
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    user = relationship("User", back_populates="cvs")
    skills = relationship("CVSkill", back_populates="cv")
    matches = relationship("Match", back_populates="cv")