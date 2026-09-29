"""Pydantic schemas for Match-related API I/O."""
from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class SkillGapOut(BaseModel):
    id: int
    skill: str
    gap_type: str        # matched / partial / missing
    importance: float
    recommendation: Optional[str] = None
    similarity_score: Optional[float] = None

    class Config:
        from_attributes = True


class MatchResultOut(BaseModel):
    id: int
    student_id: int
    internship_id: int

    overall_score: float
    skill_score: float
    education_score: float
    project_score: float
    experience_score: float
    location_score: float
    availability_score: float

    education_eligible: bool
    experience_eligible: bool
    location_eligible: bool
    availability_eligible: bool

    summary: Optional[str] = None
    explanation: Optional[List[str]] = None
    skill_gaps: List[SkillGapOut] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MatchRequest(BaseModel):
    student_id: int
    internship_id: int


class WhatIfRequest(BaseModel):
    student_id: int
    internship_id: int
    hypothetical_skills: List[str]


class WhatIfResponse(BaseModel):
    current_score: float
    projected_score: float
    improvement: float
    changed_gaps: List[Dict[str, Any]]
    note: str = (
        "This is a simulated projection based on the selected skills. "
        "It does not represent a guaranteed hiring probability."
    )


class CompareRequest(BaseModel):
    student_id: int
    internship_ids: List[int]


class DashboardData(BaseModel):
    student_id: int
    profile_completion: float
    total_skills: int
    recommended_count: int
    eligible_count: int
    average_match: float
    top_skill_gaps: List[str]
    recent_matches: List[Dict[str, Any]]
