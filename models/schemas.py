from pydantic import BaseModel, Field
from typing import List

class CandidateInput(BaseModel):
    name: str = "Candidate"
    education: str = ""
    skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    portfolio_text: str = ""
    github_username: str | None = None
    github_summary: str = ""

class RecommendationItem(BaseModel):
    track: str
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    explanation: str

class RecommendationResponse(BaseModel):
    recommended_track: str
    skill_match_score: float
    strength_analysis: List[str]
    weakness_analysis: List[str]
    missing_skills: List[str]
    mentor_recommendation: str
    confidence_score: float
    reasoning_summary: str
    roadmap: List[str]
    alternatives: List[RecommendationItem]
