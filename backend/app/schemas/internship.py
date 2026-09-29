"""Pydantic schemas for Internship-related API I/O."""
from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


# ── Requirement schemas ───────────────────────────────────────────────────────

class RequirementCreate(BaseModel):
    requirement: str
    category: Optional[str] = "skill"
    mandatory: Optional[bool] = True
    importance: Optional[float] = 1.0


class RequirementOut(RequirementCreate):
    id: int
    internship_id: int

    class Config:
        from_attributes = True


# ── Internship schemas ────────────────────────────────────────────────────────

class InternshipCreate(BaseModel):
    company: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = "remote"
    duration: Optional[str] = None
    stipend: Optional[str] = None
    deadline: Optional[str] = None
    domain: Optional[str] = None
    experience_required: Optional[str] = "Freshers"
    education_required: Optional[str] = None
    requirements: Optional[List[RequirementCreate]] = []


class InternshipUpdate(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None
    duration: Optional[str] = None
    stipend: Optional[str] = None
    deadline: Optional[str] = None
    domain: Optional[str] = None
    experience_required: Optional[str] = None
    education_required: Optional[str] = None


class InternshipOut(BaseModel):
    id: int
    company: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None
    duration: Optional[str] = None
    stipend: Optional[str] = None
    deadline: Optional[str] = None
    domain: Optional[str] = None
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    is_active: bool = True
    is_sample: bool = False
    created_at: Optional[datetime] = None
    requirements: List[RequirementOut] = []

    class Config:
        from_attributes = True


# ── Description analysis schema ───────────────────────────────────────────────

class DescriptionAnalyzeRequest(BaseModel):
    description: str


class DescriptionAnalyzeResponse(BaseModel):
    skills: List[str]
    education: List[str]
    experience: List[str]
    location: List[str]
    availability: List[str]
    preferred_skills: List[str]
    mandatory_requirements: List[str]
    raw_requirements: List[RequirementCreate]
