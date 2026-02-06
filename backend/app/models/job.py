from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    location = Column(String(255))
    description = Column(Text)
    requirements = Column(Text)
    embedding = Column(JSON)  # BERT embedding vektörü
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    skills = relationship("JobSkill", back_populates="job")
    matches = relationship("Match", back_populates="job")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))
    normalized_name = Column(String(100))

    # İlişkiler
    cv_skills = relationship("CVSkill", back_populates="skill")
    job_skills = relationship("JobSkill", back_populates="skill")


class CVSkill(Base):
    __tablename__ = "cv_skills"

    id = Column(Integer, primary_key=True, index=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    confidence_score = Column(Float, default=1.0)

    # İlişkiler
    cv = relationship("CV", back_populates="skills")
    skill = relationship("Skill", back_populates="cv_skills")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    importance = Column(Float, default=1.0)

    # İlişkiler
    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill", back_populates="job_skills")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    skill_match_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişkiler
    cv = relationship("CV", back_populates="matches")
    job = relationship("Job", back_populates="matches")