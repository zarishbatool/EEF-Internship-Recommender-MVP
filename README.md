# EEF Intelligent Internship Recommendation & Candidate Matching Engine

AI-001 implementation for the Ezitech Engineering Framework case study.

## Features

- Candidate profile processing
- Resume PDF text extraction
- Technical skill matching
- TF-IDF semantic similarity
- Internship track recommendation
- Mentor recommendation
- Skill match score
- Confidence score
- Strength and weakness analysis
- Missing skill detection
- Personalized learning roadmap
- Alternative internship tracks
- GitHub profile/repository analysis
- FastAPI REST API
- Streamlit dashboard

## Architecture

Candidate Profile / Resume / GitHub
        |
        v
Data Ingestion
        |
        v
Profile Processing + Skill Matching
        |
        +---- TF-IDF Semantic Similarity
        |
        +---- Explicit Skill Coverage
        |
        v
Recommendation Engine
        |
        +---- Internship Track
        +---- Mentor
        +---- Missing Skills
        +---- Confidence
        +---- Roadmap
        |
        v
FastAPI + Streamlit

## Installation

Python 3.11–3.13 is recommended for the smoothest dependency compatibility.

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run API

```bash
uvicorn app.main:app --reload
```

Open:
http://127.0.0.1:8000/docs

## Run Dashboard

Open another PowerShell window in the same project:

```bash
venv\Scripts\activate
streamlit run app/streamlit_app.py
```

## API

### POST /api/recommend

Example:

```json
{
  "name": "Ali",
  "education": "BS Artificial Intelligence",
  "skills": ["Python", "Machine Learning", "Pandas", "SQL"],
  "interests": ["AI", "Generative AI"],
  "certifications": ["Python"],
  "portfolio_text": "Built ML and RAG applications."
}
```

### POST /api/recommend/resume

Upload a PDF resume. Optionally provide a GitHub username.

## Important

This is a production-oriented MVP architecture. Before real organizational deployment, add authentication, PostgreSQL, proper vector search, model/version tracking, evaluation datasets, audit logs, human approval workflow, privacy controls, rate limiting and monitoring.
