"""SQLAlchemy ORM models for Internship-related entities."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(300), nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    location = Column(String(200))
    work_mode = Column(String(50))          # remote / onsite / hybrid
    duration = Column(String(100))          # "3 months", "6 months"
    stipend = Column(String(100))           # "₹15,000/month"
    deadline = Column(String(100))
    domain = Column(String(100))            # "Data Science", "Web Dev"
    experience_required = Column(String(100))   # "0-1 years", "Freshers"
    education_required = Column(String(200))    # "B.Tech CSE"
    is_active = Column(Boolean, default=True)
    is_sample = Column(Boolean, default=False)  # pre-loaded sample data
    source_url = Column(String(500))

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    requirements = relationship("InternshipRequirement", back_populates="internship", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="internship")


class InternshipRequirement(Base):
    __tablename__ = "internship_requirements"

    id = Column(Integer, primary_key=True, index=True)
    internship_id = Column(Integer, ForeignKey("internships.id"), nullable=False)
    requirement = Column(String(300), nullable=False)
    category = Column(String(100))          # skill / education / experience / location / availability / preferred
    mandatory = Column(Boolean, default=True)
    importance = Column(Float, default=1.0) # 0.0-1.0 weight

    internship = relationship("Internship", back_populates="requirements")
