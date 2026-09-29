"""Pydantic schemas for Student-related API I/O."""
from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


# ── Skill schemas ────────────────────────────────────────────────────────────

class StudentSkillCreate(BaseModel):
    skill_name: str
    category: Optional[str] = None
    proficiency: Optional[str] = "intermediate"
    evidence: Optional[str] = None
    years_experience: Optional[float] = 0


class StudentSkillOut(StudentSkillCreate):
    id: int
    student_id: int

    class Config:
        from_attributes = True


# ── Project schemas ───────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    technologies: Optional[str] = None   # comma-separated
    url: Optional[str] = None
    github_url: Optional[str] = None
    duration: Optional[str] = None


class ProjectOut(ProjectCreate):
    id: int
    student_id: int

    class Config:
        from_attributes = True


# ── Experience schemas ────────────────────────────────────────────────────────

class ExperienceCreate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: Optional[bool] = False


class ExperienceOut(ExperienceCreate):
    id: int
    student_id: int

    class Config:
        from_attributes = True


# ── Certification schemas ─────────────────────────────────────────────────────

class CertificationCreate(BaseModel):
    name: str
    issuer: Optional[str] = None
    date_obtained: Optional[str] = None
    credential_url: Optional[str] = None


class CertificationOut(CertificationCreate):
    id: int
    student_id: int

    class Config:
        from_attributes = True


# ── Student schemas ───────────────────────────────────────────────────────────

class StudentCreate(BaseModel):
    name: str
    email: str
    password: Optional[str] = "demo"
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    location: Optional[str] = None
    preferred_location: Optional[str] = None
    remote_preference: Optional[str] = "open"
    availability: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    location: Optional[str] = None
    preferred_location: Optional[str] = None
    remote_preference: Optional[str] = None
    availability: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    location: Optional[str] = None
    preferred_location: Optional[str] = None
    remote_preference: Optional[str] = None
    availability: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    created_at: Optional[datetime] = None

    skills: List[StudentSkillOut] = []
    projects: List[ProjectOut] = []
    experiences: List[ExperienceOut] = []
    certifications: List[CertificationOut] = []

    class Config:
        from_attributes = True


# ── Auth schemas ──────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    student_id: int
    name: str
    email: str
    message: str = "Login successful"
