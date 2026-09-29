"""Match engine and what-if analysis routes.

Phase 1: Rule-based scoring with configurable weights.
Phase 5: Upgraded to semantic embedding similarity.
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models.student import Student, StudentSkill, Project
from app.models.internship import Internship, InternshipRequirement
from app.models.match import MatchResult, SkillGap
from app.schemas.match import (
    MatchRequest, MatchResultOut, WhatIfRequest, WhatIfResponse,
    CompareRequest,
)

router = APIRouter(prefix="/api/match", tags=["match"])

# ── Scoring weights (configurable) ───────────────────────────────────────────

WEIGHTS = {
    "skill": 0.35,
    "education": 0.20,
    "project": 0.15,
    "experience": 0.10,
    "location": 0.10,
    "availability": 0.10,
}

# ── Skill action recommendations ──────────────────────────────────────────────

SKILL_RECOMMENDATIONS: Dict[str, str] = {
    "docker": "Learn Docker fundamentals and containerize one existing Python project.",
    "rest api": "Build a FastAPI REST API with CRUD operations and deploy it.",
    "kubernetes": "Complete 'Kubernetes for Beginners' and deploy a 2-service app on minikube.",
    "react": "Build a React + FastAPI dashboard that consumes a REST API.",
    "next.js": "Create a Next.js portfolio site with SSR and API routes.",
    "aws": "Complete AWS Cloud Practitioner and deploy a static site on S3.",
    "gcp": "Deploy a Python app on Google Cloud Run with a CI/CD pipeline.",
    "azure": "Set up an Azure Web App and integrate it with GitHub Actions.",
    "machine learning": "Build and deploy an end-to-end ML model using scikit-learn and FastAPI.",
    "deep learning": "Train a CNN image classifier using PyTorch and publish the code on GitHub.",
    "tensorflow": "Complete TensorFlow Developer Certificate and build a classification project.",
    "pytorch": "Build a sequence classification model with PyTorch and HuggingFace.",
    "nlp": "Build a text summarizer or sentiment analyzer using HuggingFace Transformers.",
    "computer vision": "Build an object detection app with YOLO or OpenCV.",
    "sql": "Complete 'SQL for Data Analysis' and build a data-driven dashboard.",
    "postgresql": "Set up a PostgreSQL database and connect it to a FastAPI backend.",
    "mongodb": "Build a Node.js/FastAPI backend using MongoDB and Mongoose/Motor.",
    "graphql": "Implement a GraphQL API for an existing REST service.",
    "microservices": "Decompose a monolith into 3 microservices using FastAPI + Docker Compose.",
    "ci/cd": "Set up a GitHub Actions pipeline that tests, builds, and deploys your project.",
    "kubernetes": "Deploy a multi-container app using Kubernetes on Minikube.",
    "pandas": "Complete a data cleaning project using Pandas and publish on Kaggle.",
    "numpy": "Implement 5 ML algorithms from scratch using NumPy.",
    "typescript": "Convert an existing JavaScript project to TypeScript.",
    "java": "Build a Spring Boot REST API and connect it to a MySQL database.",
    "spring boot": "Build a CRUD application with Spring Boot, JPA, and PostgreSQL.",
    "angular": "Build an Angular dashboard consuming a REST API.",
    "vue": "Build a Vue.js SPA for a product catalog with Vuex state management.",
    "figma": "Design 3 mobile app screens in Figma with interactive prototypes.",
    "power bi": "Build a sales analytics dashboard in Power BI from CSV data.",
    "selenium": "Automate a web form submission and test a 5-page user journey.",
    "kafka": "Set up a Kafka producer/consumer pair for real-time event streaming.",
    "linux": "Complete Linux Command Line fundamentals and set up a VPS on DigitalOcean.",
}

DEFAULT_RECOMMENDATION = "Build a project that demonstrates this skill and publish it on GitHub."


@router.post("/", response_model=MatchResultOut)
def calculate_match(payload: MatchRequest, db: Session = Depends(get_db)):
    student = _get_or_404(db, Student, payload.student_id, "Student")
    internship = _get_or_404(db, Internship, payload.internship_id, "Internship")

    result = _run_matching(student, internship, db)
    db.add(result)
    db.flush()

    # Save skill gaps
    for gap in result._gaps:  # type: ignore[attr-defined]
        gap.match_id = result.id
        db.add(gap)

    db.commit()
    db.refresh(result)
    return _serialize_match(result)


@router.get("/{match_id}", response_model=MatchResultOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = _get_or_404(db, MatchResult, match_id, "Match result")
    return _serialize_match(match)


@router.get("/student/{student_id}", response_model=List[MatchResultOut])
def get_student_matches(student_id: int, db: Session = Depends(get_db)):
    _get_or_404(db, Student, student_id, "Student")
    results = db.query(MatchResult).filter(MatchResult.student_id == student_id).all()
    return [_serialize_match(r) for r in results]


@router.post("/what-if", response_model=WhatIfResponse)
def what_if(payload: WhatIfRequest, db: Session = Depends(get_db)):
    student = _get_or_404(db, Student, payload.student_id, "Student")
    internship = _get_or_404(db, Internship, payload.internship_id, "Internship")

    # Current match
    current_result = _run_matching(student, internship, db)
    current_score = current_result.overall_score

    # Simulated match — temporarily augment student skills
    hypo_skills = [
        StudentSkill(student_id=student.id, skill_name=s, category="hypothetical")
        for s in payload.hypothetical_skills
    ]
    original_skills = list(student.skills)
    student.skills = original_skills + hypo_skills

    projected_result = _run_matching(student, internship, db)
    projected_score = projected_result.overall_score

    # Restore original skills (don't persist hypothetical)
    student.skills = original_skills

    changed = []
    for gap in current_result._gaps:  # type: ignore[attr-defined]
        if gap.skill.lower() in [s.lower() for s in payload.hypothetical_skills]:
            changed.append({"skill": gap.skill, "before": gap.gap_type, "after": "matched"})

    return WhatIfResponse(
        current_score=round(current_score, 1),
        projected_score=round(projected_score, 1),
        improvement=round(projected_score - current_score, 1),
        changed_gaps=changed,
    )


@router.post("/compare")
def compare_internships(payload: CompareRequest, db: Session = Depends(get_db)):
    student = _get_or_404(db, Student, payload.student_id, "Student")
    results = []
    for iid in payload.internship_ids:
        internship = db.query(Internship).filter(Internship.id == iid).first()
        if not internship:
            continue
        match = _run_matching(student, internship, db)
        results.append({
            "internship_id": iid,
            "company": internship.company,
            "title": internship.title,
            "location": internship.location,
            "work_mode": internship.work_mode,
            "overall_score": round(match.overall_score, 1),
            "skill_score": round(match.skill_score, 1),
            "education_score": round(match.education_score, 1),
            "project_score": round(match.project_score, 1),
            "experience_score": round(match.experience_score, 1),
            "location_score": round(match.location_score, 1),
            "education_eligible": match.education_eligible,
            "experience_eligible": match.experience_eligible,
            "location_eligible": match.location_eligible,
            "missing_skills": [g.skill for g in match._gaps if g.gap_type == "missing"],  # type: ignore
        })
    results.sort(key=lambda x: x["overall_score"], reverse=True)
    return {"comparisons": results}


# ── Core matching engine ──────────────────────────────────────────────────────

def _run_matching(student: Student, internship: Internship, db: Session) -> MatchResult:
    """Calculate all component scores and build a MatchResult object."""
    student_skill_names = {s.skill_name.lower() for s in student.skills}
    student_tech = _extract_tech_from_projects(student.projects)

    requirements = internship.requirements
    skill_reqs = [r for r in requirements if r.category == "skill"]
    edu_reqs = [r for r in requirements if r.category == "education"]
    exp_reqs = [r for r in requirements if r.category == "experience"]
    loc_reqs = [r for r in requirements if r.category == "location"]
    avail_reqs = [r for r in requirements if r.category == "availability"]

    # ── Skill matching ────────────────────────────────────────────────────────
    gaps: List[SkillGap] = []
    matched = 0
    partial = 0
    total_skill_weight = sum(r.importance for r in skill_reqs) or 1

    for req in skill_reqs:
        req_lower = req.requirement.lower()
        gap_type, similarity = _match_skill(req_lower, student_skill_names, student_tech)
        rec = SKILL_RECOMMENDATIONS.get(req_lower, DEFAULT_RECOMMENDATION)

        gaps.append(SkillGap(
            skill=req.requirement,
            gap_type=gap_type,
            importance=req.importance,
            recommendation=rec if gap_type != "matched" else None,
            similarity_score=similarity,
        ))

        if gap_type == "matched":
            matched += req.importance
        elif gap_type == "partial":
            partial += req.importance * 0.5

    skill_score = ((matched + partial) / total_skill_weight) * 100 if skill_reqs else 80.0

    # ── Education matching ────────────────────────────────────────────────────
    edu_score, edu_eligible = _score_education(student, internship, edu_reqs)

    # ── Project relevance ─────────────────────────────────────────────────────
    project_score = _score_projects(student.projects, skill_reqs, student_tech)

    # ── Experience matching ───────────────────────────────────────────────────
    exp_score, exp_eligible = _score_experience(student, internship, exp_reqs)

    # ── Location matching ─────────────────────────────────────────────────────
    loc_score, loc_eligible = _score_location(student, internship, loc_reqs)

    # ── Availability matching ─────────────────────────────────────────────────
    avail_score, avail_eligible = _score_availability(student, internship, avail_reqs)

    # ── Weighted overall ──────────────────────────────────────────────────────
    overall = (
        skill_score * WEIGHTS["skill"]
        + edu_score * WEIGHTS["education"]
        + project_score * WEIGHTS["project"]
        + exp_score * WEIGHTS["experience"]
        + loc_score * WEIGHTS["location"]
        + avail_score * WEIGHTS["availability"]
    )

    # Build explanation
    explanation = _build_explanation(
        gaps, edu_eligible, exp_eligible, loc_eligible, avail_eligible, student, internship
    )

    summary = (
        f"Based on your profile, you match approximately {overall:.0f}% of the requirements "
        f"for the {internship.title} position at {internship.company}. "
        f"This score reflects compatibility with available requirements and is not a hiring probability."
    )

    result = MatchResult(
        student_id=student.id,
        internship_id=internship.id,
        overall_score=round(overall, 2),
        skill_score=round(skill_score, 2),
        education_score=round(edu_score, 2),
        project_score=round(project_score, 2),
        experience_score=round(exp_score, 2),
        location_score=round(loc_score, 2),
        availability_score=round(avail_score, 2),
        education_eligible=edu_eligible,
        experience_eligible=exp_eligible,
        location_eligible=loc_eligible,
        availability_eligible=avail_eligible,
        explanation_json=json.dumps(explanation),
        summary=summary,
    )
    result._gaps = gaps  # type: ignore[attr-defined]
    return result


def _match_skill(req: str, student_skills: set, project_tech: set) -> tuple[str, float]:
    """Simple skill matching with alias expansion. Phase 5 upgrades to embeddings."""
    ALIASES = {
        "machine learning": {"ml", "scikit-learn", "sklearn", "regression", "classification", "model training", "random forest"},
        "deep learning": {"neural network", "cnn", "rnn", "lstm", "tensorflow", "pytorch", "keras"},
        "rest api": {"fastapi", "flask", "django rest", "api development", "http api", "restful"},
        "docker": {"containerization", "container"},
        "sql": {"mysql", "postgresql", "sqlite", "database query"},
        "nlp": {"natural language processing", "spacy", "nltk", "transformers", "bert"},
        "computer vision": {"opencv", "image processing", "yolo", "object detection"},
        "aws": {"amazon web services", "s3", "ec2", "lambda", "cloud"},
        "react": {"reactjs", "react.js"},
        "next.js": {"nextjs"},
        "node.js": {"nodejs"},
        "javascript": {"js"},
        "typescript": {"ts"},
    }

    # Direct match
    if req in student_skills:
        return "matched", 1.0

    # Check aliases
    aliases = ALIASES.get(req, set())
    for alias in aliases:
        if alias in student_skills or alias in project_tech:
            return "partial", 0.7

    # Partial text match (e.g. "python" in "python 3.10")
    for s in student_skills:
        if req in s or s in req:
            return "partial", 0.6

    # Project tech match
    if req in project_tech:
        return "partial", 0.5

    return "missing", 0.0


def _extract_tech_from_projects(projects: List[Project]) -> set:
    tech = set()
    for p in projects:
        if p.technologies:
            for t in p.technologies.replace(",", " ").split():
                tech.add(t.lower().strip())
    return tech


def _score_education(student: Student, internship: Internship, edu_reqs: list) -> tuple[float, bool]:
    if not edu_reqs:
        return 90.0, True

    student_degree = (student.degree or "").lower()
    student_branch = (student.branch or "").lower()

    matched = 0
    for req in edu_reqs:
        r = req.requirement.lower()
        if any(kw in student_degree or kw in student_branch for kw in r.split()):
            matched += 1

    ratio = matched / len(edu_reqs) if edu_reqs else 1.0
    eligible = ratio >= 0.5
    return ratio * 100, eligible


def _score_experience(student: Student, internship: Internship, exp_reqs: list) -> tuple[float, bool]:
    fresher_terms = {"fresher", "0-1 year", "0 to 1", "no experience", "freshers allowed"}
    exp_text = (internship.experience_required or "").lower()

    if any(t in exp_text for t in fresher_terms):
        return 100.0, True

    has_experience = len(student.experiences) > 0
    if has_experience:
        return 85.0, True

    return 60.0, True  # No experience but internship doesn't strictly require it


def _score_location(student: Student, internship: Internship, loc_reqs: list) -> tuple[float, bool]:
    if internship.work_mode in ("remote", "Remote"):
        return 100.0, True

    student_loc = (student.location or "").lower()
    student_pref = (student.preferred_location or "").lower()
    internship_loc = (internship.location or "").lower()
    student_remote = (student.remote_preference or "").lower()

    if "remote" in internship_loc:
        return 100.0, True

    if student_loc in internship_loc or internship_loc in student_loc:
        return 100.0, True

    if student_pref in internship_loc or internship_loc in student_pref:
        return 90.0, True

    if student_remote == "open":
        return 70.0, True

    return 50.0, False


def _score_availability(student: Student, internship: Internship, avail_reqs: list) -> tuple[float, bool]:
    if not student.availability or not avail_reqs:
        return 80.0, True

    student_avail = student.availability.lower()
    for req in avail_reqs:
        if req.requirement.lower() in student_avail or student_avail in req.requirement.lower():
            return 100.0, True

    return 70.0, True


def _score_projects(projects: List[Project], skill_reqs: list, project_tech: set) -> float:
    if not projects:
        return 40.0
    if not skill_reqs:
        return 80.0

    req_skills = {r.requirement.lower() for r in skill_reqs}
    overlap = req_skills & project_tech
    ratio = len(overlap) / len(req_skills) if req_skills else 0
    base = min(40 + len(projects) * 10, 70)   # more projects = higher base
    return min(base + ratio * 30, 100.0)


def _build_explanation(gaps, edu_elig, exp_elig, loc_elig, avail_elig, student, internship) -> list:
    explanation = []

    matched_skills = [g.skill for g in gaps if g.gap_type == "matched"]
    partial_skills = [g.skill for g in gaps if g.gap_type == "partial"]
    missing_skills = [g.skill for g in gaps if g.gap_type == "missing"]

    if matched_skills:
        explanation.append({"type": "positive", "text": f"Matched skills: {', '.join(matched_skills)}"})
    if partial_skills:
        explanation.append({"type": "warning", "text": f"Partially matched (related skills found): {', '.join(partial_skills)}"})
    if missing_skills:
        explanation.append({"type": "negative", "text": f"Missing skills: {', '.join(missing_skills)}"})

    explanation.append({"type": "positive" if edu_elig else "negative", "text": f"Education requirement: {'satisfied' if edu_elig else 'not satisfied'}"})
    explanation.append({"type": "positive" if exp_elig else "negative", "text": f"Experience requirement: {'satisfied' if exp_elig else 'not satisfied'}"})
    explanation.append({"type": "positive" if loc_elig else "warning", "text": f"Location compatibility: {'compatible' if loc_elig else 'may require relocation'}"})
    explanation.append({"type": "positive" if avail_elig else "warning", "text": f"Availability: {'compatible' if avail_elig else 'check availability requirements'}"})

    return explanation


def _serialize_match(result: MatchResult) -> MatchResultOut:
    explanation = []
    if result.explanation_json:
        try:
            explanation = json.loads(result.explanation_json)
        except Exception:
            pass

    return MatchResultOut(
        id=result.id,
        student_id=result.student_id,
        internship_id=result.internship_id,
        overall_score=result.overall_score,
        skill_score=result.skill_score,
        education_score=result.education_score,
        project_score=result.project_score,
        experience_score=result.experience_score,
        location_score=result.location_score,
        availability_score=result.availability_score,
        education_eligible=result.education_eligible,
        experience_eligible=result.experience_eligible,
        location_eligible=result.location_eligible,
        availability_eligible=result.availability_eligible,
        summary=result.summary,
        explanation=explanation,
        skill_gaps=[
            {  # type: ignore
                "id": g.id or 0,
                "skill": g.skill,
                "gap_type": g.gap_type,
                "importance": g.importance,
                "recommendation": g.recommendation,
                "similarity_score": g.similarity_score,
            }
            for g in result.skill_gaps
        ],
        created_at=result.created_at,
    )


def _get_or_404(db: Session, model, id: int, name: str):
    obj = db.query(model).filter(model.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{name} not found")
    return obj
