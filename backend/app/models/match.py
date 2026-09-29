"""SQLAlchemy ORM models for Match and SkillGap entities."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    internship_id = Column(Integer, ForeignKey("internships.id"), nullable=False)

    # Component scores (0-100)
    overall_score = Column(Float, default=0.0)
    skill_score = Column(Float, default=0.0)
    education_score = Column(Float, default=0.0)
    project_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    location_score = Column(Float, default=0.0)
    availability_score = Column(Float, default=0.0)

    # Eligibility flags
    education_eligible = Column(Boolean, default=True)
    experience_eligible = Column(Boolean, default=True)
    location_eligible = Column(Boolean, default=True)
    availability_eligible = Column(Boolean, default=True)

    # Explanation text (stored as JSON string)
    explanation_json = Column(Text)     # serialized list of explanation points
    summary = Column(Text)             # one-paragraph summary

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="match_results")
    internship = relationship("Internship", back_populates="match_results")
    skill_gaps = relationship("SkillGap", back_populates="match_result", cascade="all, delete-orphan")


class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("match_results.id"), nullable=False)
    skill = Column(String(200), nullable=False)
    gap_type = Column(String(50))       # matched / partial / missing
    importance = Column(Float, default=1.0)
    recommendation = Column(Text)
    similarity_score = Column(Float)    # 0-1 from NLP similarity

    match_result = relationship("MatchResult", back_populates="skill_gaps")
