"""Student CRUD API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.student import Student, StudentSkill, Project, Experience, Certification
from app.schemas.student import (
    StudentCreate, StudentUpdate, StudentOut,
    StudentSkillCreate, StudentSkillOut,
    ProjectCreate, ProjectOut,
    ExperienceCreate, ExperienceOut,
    CertificationCreate, CertificationOut,
    LoginRequest, LoginResponse,
)

router = APIRouter(prefix="/api/students", tags=["students"])


# ── Auth (MVP mock) ───────────────────────────────────────────────────────────

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == request.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    # MVP: no real password check — just return the student
    return LoginResponse(student_id=student.id, name=student.name, email=student.email)


# ── Student CRUD ──────────────────────────────────────────────────────────────

@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    student = Student(
        name=payload.name,
        email=payload.email,
        password_hash=payload.password or "demo",
        college=payload.college,
        degree=payload.degree,
        branch=payload.branch,
        graduation_year=payload.graduation_year,
        cgpa=payload.cgpa,
        location=payload.location,
        preferred_location=payload.preferred_location,
        remote_preference=payload.remote_preference,
        availability=payload.availability,
        bio=payload.bio,
        phone=payload.phone,
        linkedin=payload.linkedin,
        github=payload.github,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/", response_model=List[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()


# ── Skills ────────────────────────────────────────────────────────────────────

@router.post("/{student_id}/skills", response_model=StudentSkillOut, status_code=201)
def add_skill(student_id: int, payload: StudentSkillCreate, db: Session = Depends(get_db)):
    _require_student(student_id, db)
    skill = StudentSkill(student_id=student_id, **payload.model_dump())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/{student_id}/skills/{skill_id}", status_code=204)
def delete_skill(student_id: int, skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(StudentSkill).filter(
        StudentSkill.id == skill_id, StudentSkill.student_id == student_id
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()


@router.put("/{student_id}/skills", response_model=List[StudentSkillOut])
def replace_skills(student_id: int, payload: List[StudentSkillCreate], db: Session = Depends(get_db)):
    """Replace all skills for a student (used after resume parsing)."""
    _require_student(student_id, db)
    db.query(StudentSkill).filter(StudentSkill.student_id == student_id).delete()
    skills = [StudentSkill(student_id=student_id, **s.model_dump()) for s in payload]
    db.add_all(skills)
    db.commit()
    for s in skills:
        db.refresh(s)
    return skills


# ── Projects ──────────────────────────────────────────────────────────────────

@router.post("/{student_id}/projects", response_model=ProjectOut, status_code=201)
def add_project(student_id: int, payload: ProjectCreate, db: Session = Depends(get_db)):
    _require_student(student_id, db)
    project = Project(student_id=student_id, **payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{student_id}/projects/{project_id}", status_code=204)
def delete_project(student_id: int, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(
        Project.id == project_id, Project.student_id == student_id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()


# ── Experiences ───────────────────────────────────────────────────────────────

@router.post("/{student_id}/experiences", response_model=ExperienceOut, status_code=201)
def add_experience(student_id: int, payload: ExperienceCreate, db: Session = Depends(get_db)):
    _require_student(student_id, db)
    exp = Experience(student_id=student_id, **payload.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


# ── Certifications ────────────────────────────────────────────────────────────

@router.post("/{student_id}/certifications", response_model=CertificationOut, status_code=201)
def add_certification(student_id: int, payload: CertificationCreate, db: Session = Depends(get_db)):
    _require_student(student_id, db)
    cert = Certification(student_id=student_id, **payload.model_dump())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


# ── Helpers ───────────────────────────────────────────────────────────────────

def _require_student(student_id: int, db: Session) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
