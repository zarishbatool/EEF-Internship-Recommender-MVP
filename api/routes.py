from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import CandidateInput, RecommendationResponse
from services.resume_parser import extract_resume_text
from services.recommendation_engine import RecommendationEngine
from services.github_analyzer import analyze_github

router = APIRouter()
engine = RecommendationEngine()

@router.post("/recommend", response_model=RecommendationResponse)
def recommend(candidate: CandidateInput):
    return engine.recommend(candidate)

@router.post("/recommend/resume", response_model=RecommendationResponse)
async def recommend_from_resume(
    file: UploadFile = File(...),
    github_username: str | None = None
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported.")

    content = await file.read()
    text = extract_resume_text(content)

    github_data = {}
    if github_username:
        github_data = analyze_github(github_username)

    candidate = CandidateInput(
        name="Resume Candidate",
        education="",
        skills=[],
        interests=[],
        certifications=[],
        portfolio_text=text,
        github_username=github_username,
        github_summary=github_data.get("summary", "")
    )

    return engine.recommend(candidate)

@router.get("/tracks")
def tracks():
    return engine.tracks

@router.get("/mentors")
def mentors():
    return engine.mentors
