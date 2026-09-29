"""Resume upload and extraction stub.

Phase 1: Returns mock extracted data.
Phase 4: Upgraded to real PDF/DOCX parsing + NLP.
"""
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/resume", tags=["resume"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}
MAX_SIZE_MB = 5


class ResumeExtractResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    skills: List[str] = []
    projects: List[dict] = []
    experiences: List[dict] = []
    certifications: List[str] = []
    raw_text_preview: str = ""
    note: str = "Extraction is AI-assisted. Please verify and edit the results."


@router.post("/analyze", response_model=ResumeExtractResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Upload a resume and extract structured information.
    Phase 1: validates file type and returns a stub response.
    Phase 4: implements real PDF/DOCX parsing and NLP.
    """
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported: PDF, DOCX, DOC, TXT",
        )

    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f} MB). Maximum allowed: {MAX_SIZE_MB} MB",
        )

    # Phase 1 stub — return detected filename as name hint
    name_hint = (file.filename or "").replace(ext, "").replace("_", " ").replace("-", " ").title()

    return ResumeExtractResponse(
        name=name_hint if name_hint else None,
        raw_text_preview=f"[File '{file.filename}' received — {len(content)} bytes. NLP extraction will be enabled in Phase 4.]",
        note=(
            "Resume parsing is not yet active. "
            "Please manually enter your profile information for now. "
            "Full NLP-based extraction will be available in a future update."
        ),
    )
