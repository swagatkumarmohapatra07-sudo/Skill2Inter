"""SQLAlchemy ORM models for Student-related entities."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password_hash = Column(String(500), nullable=False, default="demo")

    # Education
    college = Column(String(300))
    degree = Column(String(100))      # B.Tech, BCA, B.Sc
    branch = Column(String(200))      # CSE, ECE, IT
    graduation_year = Column(Integer)
    cgpa = Column(Float)

    # Location & Preferences
    location = Column(String(200))
    preferred_location = Column(String(200))
    remote_preference = Column(String(50), default="open")  # remote / onsite / open
    availability = Column(String(100))   # e.g. "2 months", "immediate"

    # Profile completeness (0-100 calculated on the fly)
    bio = Column(Text)
    phone = Column(String(30))
    linkedin = Column(String(500))
    github = Column(String(500))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="student", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="student", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="student", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="student")


class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    skill_name = Column(String(200), nullable=False)
    category = Column(String(100))          # programming / ml / web / cloud / tool / soft
    proficiency = Column(String(50))        # beginner / intermediate / advanced / expert
    evidence = Column(Text)                 # "Used in Weather Prediction project"
    years_experience = Column(Float, default=0)

    student = relationship("Student", back_populates="skills")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    technologies = Column(Text)   # comma-separated or JSON string
    url = Column(String(500))
    github_url = Column(String(500))
    duration = Column(String(100))          # "3 months"

    student = relationship("Student", back_populates="projects")


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    company = Column(String(300))
    role = Column(String(300))
    description = Column(Text)
    start_date = Column(String(50))
    end_date = Column(String(50))
    is_current = Column(Boolean, default=False)

    student = relationship("Student", back_populates="experiences")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    name = Column(String(300), nullable=False)
    issuer = Column(String(300))
    date_obtained = Column(String(50))
    credential_url = Column(String(500))

    student = relationship("Student", back_populates="certifications")
