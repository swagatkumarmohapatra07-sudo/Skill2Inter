"""Internship CRUD + description analysis API routes."""
import json
import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.internship import Internship, InternshipRequirement
from app.schemas.internship import (
    InternshipCreate, InternshipUpdate, InternshipOut,
    DescriptionAnalyzeRequest, DescriptionAnalyzeResponse,
    RequirementCreate,
)

router = APIRouter(prefix="/api/internships", tags=["internships"])


# ── CRUD ──────────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[InternshipOut])
def list_internships(
    domain: Optional[str] = None,
    work_mode: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Internship).filter(Internship.is_active == True)
    if domain:
        query = query.filter(Internship.domain.ilike(f"%{domain}%"))
    if work_mode:
        query = query.filter(Internship.work_mode == work_mode)
    return query.all()


@router.get("/{internship_id}", response_model=InternshipOut)
def get_internship(internship_id: int, db: Session = Depends(get_db)):
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    return internship


@router.post("/", response_model=InternshipOut, status_code=status.HTTP_201_CREATED)
def create_internship(payload: InternshipCreate, db: Session = Depends(get_db)):
    internship = Internship(
        company=payload.company,
        title=payload.title,
        description=payload.description,
        location=payload.location,
        work_mode=payload.work_mode,
        duration=payload.duration,
        stipend=payload.stipend,
        deadline=payload.deadline,
        domain=payload.domain,
        experience_required=payload.experience_required,
        education_required=payload.education_required,
    )
    db.add(internship)
    db.flush()   # get ID before adding requirements

    for req in (payload.requirements or []):
        r = InternshipRequirement(internship_id=internship.id, **req.model_dump())
        db.add(r)

    db.commit()
    db.refresh(internship)
    return internship


@router.put("/{internship_id}", response_model=InternshipOut)
def update_internship(internship_id: int, payload: InternshipUpdate, db: Session = Depends(get_db)):
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(internship, field, value)
    db.commit()
    db.refresh(internship)
    return internship


@router.delete("/{internship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_internship(internship_id: int, db: Session = Depends(get_db)):
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    db.delete(internship)
    db.commit()


# ── Description Analysis (NLP stub — Phase 4 will use real NLP) ───────────────

@router.post("/analyze", response_model=DescriptionAnalyzeResponse)
def analyze_description(payload: DescriptionAnalyzeRequest):
    """
    Extract structured requirements from a pasted internship description.
    Phase 1: rule-based extraction.
    Phase 4: upgraded to NLP/embedding-based extraction.
    """
    text = payload.description.lower()
    original = payload.description

    skills = _extract_skills(text)
    education = _extract_education(text)
    experience = _extract_experience(text)
    location = _extract_location(text, original)
    availability = _extract_availability(text)
    preferred = _extract_preferred(text)

    # Build raw requirements list
    raw: List[RequirementCreate] = []
    for s in skills:
        raw.append(RequirementCreate(requirement=s, category="skill", mandatory=True, importance=1.0))
    for s in preferred:
        raw.append(RequirementCreate(requirement=s, category="skill", mandatory=False, importance=0.6))
    for e in education:
        raw.append(RequirementCreate(requirement=e, category="education", mandatory=True, importance=1.0))
    for e in experience:
        raw.append(RequirementCreate(requirement=e, category="experience", mandatory=False, importance=0.8))
    for loc in location:
        raw.append(RequirementCreate(requirement=loc, category="location", mandatory=False, importance=0.7))
    for a in availability:
        raw.append(RequirementCreate(requirement=a, category="availability", mandatory=True, importance=0.9))

    return DescriptionAnalyzeResponse(
        skills=skills,
        education=education,
        experience=experience,
        location=location,
        availability=availability,
        preferred_skills=preferred,
        mandatory_requirements=[r.requirement for r in raw if r.mandatory],
        raw_requirements=raw,
    )


# ── Rule-based extraction helpers ────────────────────────────────────────────

SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "golang", "rust",
    "react", "vue", "angular", "next.js", "node.js", "express",
    "fastapi", "django", "flask", "spring boot",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "keras",
    "docker", "kubernetes", "aws", "gcp", "azure",
    "git", "github", "ci/cd", "jenkins", "linux",
    "rest api", "graphql", "microservices",
    "pandas", "numpy", "matplotlib", "seaborn",
    "html", "css", "tailwind", "bootstrap",
    "figma", "ui/ux", "adobe xd",
    "excel", "power bi", "tableau",
    "selenium", "cypress", "pytest",
    "kafka", "rabbitmq", "airflow",
]

EDUCATION_KEYWORDS = [
    "b.tech", "btech", "be", "b.e.", "mca", "bca", "b.sc", "bsc",
    "computer science", "cse", "information technology", "it",
    "electronics", "ece", "electrical",
    "final year", "third year", "second year",
    "undergraduate", "graduate",
]

EXPERIENCE_KEYWORDS = [
    "fresher", "0-1 year", "0 to 1", "no experience", "no prior experience",
    "1-2 year", "2+ year", "6 months", "previous internship",
]

LOCATION_KEYWORDS = [
    "remote", "work from home", "wfh", "bangalore", "bengaluru", "mumbai",
    "delhi", "hyderabad", "chennai", "pune", "kolkata", "noida", "gurugram",
    "india", "pan india", "hybrid",
]

AVAILABILITY_KEYWORDS = [
    "full-time", "part-time", "3 months", "6 months", "2 months",
    "immediate joiner", "summer internship", "winter internship",
]


def _extract_skills(text: str) -> List[str]:
    found = []
    for skill in SKILL_KEYWORDS:
        if skill in text:
            found.append(skill.title().replace(" ", " "))
    return list(dict.fromkeys(found))   # preserve order, remove duplicates


def _extract_education(text: str) -> List[str]:
    found = []
    for kw in EDUCATION_KEYWORDS:
        if kw in text:
            found.append(kw.upper() if len(kw) <= 4 else kw.title())
    return list(dict.fromkeys(found))


def _extract_experience(text: str) -> List[str]:
    found = []
    for kw in EXPERIENCE_KEYWORDS:
        if kw in text:
            found.append(kw.title())
    return list(dict.fromkeys(found))


def _extract_location(text: str, original: str) -> List[str]:
    found = []
    for kw in LOCATION_KEYWORDS:
        if kw in text:
            # Preserve original casing for city names
            found.append(kw.title())
    return list(dict.fromkeys(found))


def _extract_availability(text: str) -> List[str]:
    found = []
    for kw in AVAILABILITY_KEYWORDS:
        if kw in text:
            found.append(kw.title())
    return list(dict.fromkeys(found))


def _extract_preferred(text: str) -> List[str]:
    """Detect skills in 'preferred'/'good to have'/'nice to have' sections."""
    preferred_section = ""
    patterns = [r"preferred[:\s]+(.*?)(?=\n\n|\Z)", r"good to have[:\s]+(.*?)(?=\n\n|\Z)", r"nice to have[:\s]+(.*?)(?=\n\n|\Z)"]
    for pat in patterns:
        match = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if match:
            preferred_section += " " + match.group(1)

    if not preferred_section:
        return []

    found = []
    for skill in SKILL_KEYWORDS:
        if skill in preferred_section:
            found.append(skill.title())
    return list(dict.fromkeys(found))
