from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(
    title="EEF Intelligent Internship Recommendation Engine",
    version="1.0.0",
    description="AI-powered internship, mentor and learning-roadmap recommendation API."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "project": "EEF AI-001",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
