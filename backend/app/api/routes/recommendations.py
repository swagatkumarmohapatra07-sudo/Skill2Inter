"""Recommendations and Dashboard routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models.student import Student
from app.models.internship import Internship
from app.models.match import MatchResult
from app.api.routes.match import _run_matching, _get_or_404

router = APIRouter(tags=["recommendations"])


@router.get("/api/recommendations/{student_id}")
def get_recommendations(student_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """
    Return top internship matches for a student, sorted by overall_score.
    Runs matching engine on all active internships if no prior match result exists.
    """
    student = _get_or_404(db, Student, student_id, "Student")
    internships = db.query(Internship).filter(Internship.is_active == True).all()

    recommendations = []
    for internship in internships:
        # Check for existing match result (avoid recomputing every time)
        existing = db.query(MatchResult).filter(
            MatchResult.student_id == student_id,
            MatchResult.internship_id == internship.id,
        ).order_by(MatchResult.created_at.desc()).first()

        if existing:
            match = existing
            gaps = existing.skill_gaps
        else:
            match = _run_matching(student, internship, db)
            gaps = match._gaps  # type: ignore[attr-defined]

        missing_skills = [g.skill for g in gaps if g.gap_type == "missing"]
        matched_skills = [g.skill for g in gaps if g.gap_type == "matched"]

        recommendations.append({
            "internship_id": internship.id,
            "company": internship.company,
            "title": internship.title,
            "domain": internship.domain,
            "location": internship.location,
            "work_mode": internship.work_mode,
            "duration": internship.duration,
            "stipend": internship.stipend,
            "overall_score": round(match.overall_score, 1),
            "skill_score": round(match.skill_score, 1),
            "education_eligible": match.education_eligible,
            "experience_eligible": match.experience_eligible,
            "location_eligible": match.location_eligible,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "missing_count": len(missing_skills),
            "match_id": getattr(match, "id", None),
        })

    # Sort: eligible first, then by score
    recommendations.sort(
        key=lambda x: (
            x["education_eligible"],
            x["overall_score"],
        ),
        reverse=True,
    )

    return {"student_id": student_id, "recommendations": recommendations[:limit]}


@router.get("/api/dashboard/{student_id}")
def get_dashboard(student_id: int, db: Session = Depends(get_db)):
    student = _get_or_404(db, Student, student_id, "Student")

    total_skills = len(student.skills)
    profile_fields = [
        student.name, student.email, student.college, student.degree,
        student.branch, student.graduation_year, student.location,
        student.availability,
    ]
    filled = sum(1 for f in profile_fields if f)
    profile_completion = round(filled / len(profile_fields) * 100)

    # Get all existing match results
    matches = db.query(MatchResult).filter(MatchResult.student_id == student_id).all()
    avg_match = round(sum(m.overall_score for m in matches) / len(matches), 1) if matches else 0
    eligible_count = sum(
        1 for m in matches if m.education_eligible and m.experience_eligible
    )

    # Top skill gaps across all recent matches
    from app.models.match import SkillGap
    all_gaps = db.query(SkillGap).join(MatchResult).filter(
        MatchResult.student_id == student_id,
        SkillGap.gap_type == "missing",
    ).all()

    gap_counts: Dict[str, int] = {}
    for gap in all_gaps:
        gap_counts[gap.skill] = gap_counts.get(gap.skill, 0) + 1

    top_gaps = sorted(gap_counts, key=gap_counts.get, reverse=True)[:5]  # type: ignore[arg-type]

    # Recent matches
    recent = sorted(matches, key=lambda m: m.created_at or 0, reverse=True)[:5]
    recent_data = []
    for m in recent:
        internship = db.query(Internship).filter(Internship.id == m.internship_id).first()
        if internship:
            recent_data.append({
                "match_id": m.id,
                "internship_id": m.internship_id,
                "company": internship.company,
                "title": internship.title,
                "score": round(m.overall_score, 1),
                "created_at": m.created_at.isoformat() if m.created_at else None,
            })

    return {
        "student_id": student_id,
        "name": student.name,
        "profile_completion": profile_completion,
        "total_skills": total_skills,
        "total_projects": len(student.projects),
        "recommended_count": len(matches),
        "eligible_count": eligible_count,
        "average_match": avg_match,
        "top_skill_gaps": top_gaps,
        "recent_matches": recent_data,
    }
