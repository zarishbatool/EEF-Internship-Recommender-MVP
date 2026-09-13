from models.schemas import CandidateInput
from services.recommendation_engine import RecommendationEngine

def test_ml_recommendation():
    engine = RecommendationEngine()

    candidate = CandidateInput(
        name="Test",
        education="BS AI",
        skills=["Python", "Machine Learning", "Pandas", "NumPy", "Scikit-learn"],
        interests=["AI", "Machine Learning"],
        portfolio_text="Built machine learning projects."
    )

    result = engine.recommend(candidate)

    assert result["recommended_track"] in [
        "AI / Machine Learning",
        "Data Science",
        "Generative AI / LLM Engineering"
    ]
    assert 0 <= result["skill_match_score"] <= 100
    assert 0 <= result["confidence_score"] <= 100
