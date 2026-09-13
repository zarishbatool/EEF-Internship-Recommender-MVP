from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class RecommendationEngine:
    def __init__(self):
        self.tracks = [
            {
                "name": "AI / Machine Learning",
                "skills": ["python", "machine learning", "numpy", "pandas", "scikit-learn",
                           "tensorflow", "pytorch", "nlp", "deep learning", "sql"],
                "keywords": "python machine learning data science pandas numpy sklearn tensorflow pytorch nlp deep learning"
            },
            {
                "name": "Data Science",
                "skills": ["python", "pandas", "numpy", "sql", "statistics", "matplotlib",
                           "seaborn", "scikit-learn", "data analysis", "machine learning"],
                "keywords": "python pandas numpy sql statistics data analysis visualization machine learning"
            },
            {
                "name": "Web / Full Stack Development",
                "skills": ["html", "css", "javascript", "react", "node.js", "django",
                           "fastapi", "flask", "sql", "git", "rest api"],
                "keywords": "html css javascript react node django fastapi flask sql git api full stack"
            },
            {
                "name": "Generative AI / LLM Engineering",
                "skills": ["python", "llm", "rag", "langchain", "embeddings", "vector database",
                           "pinecone", "transformers", "prompt engineering", "nlp"],
                "keywords": "python llm rag embeddings vector database pinecone transformers nlp prompts"
            },
            {
                "name": "AI Computer Vision",
                "skills": ["python", "opencv", "computer vision", "cnn", "tensorflow",
                           "pytorch", "image processing", "deep learning"],
                "keywords": "python opencv computer vision cnn tensorflow pytorch image processing deep learning"
            }
        ]

        self.mentors = [
            {"name": "AI/ML Mentor", "track": "AI / Machine Learning",
             "skills": ["python", "machine learning", "pytorch", "tensorflow"]},
            {"name": "Data Science Mentor", "track": "Data Science",
             "skills": ["python", "pandas", "sql", "statistics"]},
            {"name": "Full Stack Mentor", "track": "Web / Full Stack Development",
             "skills": ["javascript", "react", "django", "fastapi", "sql"]},
            {"name": "GenAI/RAG Mentor", "track": "Generative AI / LLM Engineering",
             "skills": ["python", "rag", "llm", "embeddings", "pinecone"]},
            {"name": "Computer Vision Mentor", "track": "AI Computer Vision",
             "skills": ["opencv", "computer vision", "pytorch", "tensorflow"]}
        ]

    def normalize(self, value: str) -> str:
        value = value.lower().replace("-", " ")
        value = re.sub(r"[^a-z0-9+#. ]", " ", value)
        return re.sub(r"\s+", " ", value).strip()

    def candidate_text(self, c):
        parts = [
            c.education,
            " ".join(c.skills),
            " ".join(c.interests),
            " ".join(c.certifications),
            c.portfolio_text,
            c.github_summary
        ]
        return self.normalize(" ".join(parts))

    def skill_matches(self, candidate_text, track):
        matched, missing = [], []
        for skill in track["skills"]:
            s = self.normalize(skill)
            if s in candidate_text:
                matched.append(skill)
            else:
                missing.append(skill)
        return matched, missing

    def recommend(self, candidate):
        text = self.candidate_text(candidate)

        corpus = [text] + [self.normalize(t["keywords"]) for t in self.tracks]
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        matrix = vectorizer.fit_transform(corpus)
        similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

        results = []
        for idx, track in enumerate(self.tracks):
            matched, missing = self.skill_matches(text, track)

            # Blend semantic similarity with explicit skill coverage.
            skill_score = len(matched) / max(len(track["skills"]), 1)
            semantic_score = float(similarities[idx])
            final_score = (semantic_score * 0.45 + skill_score * 0.55) * 100

            results.append({
                "track": track["name"],
                "score": round(final_score, 2),
                "matched": matched,
                "missing": missing
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        best = results[0]

        mentor = self.best_mentor(best["track"], best["matched"])
        strengths = self.strengths(best)
        weaknesses = self.weaknesses(best)
        roadmap = self.make_roadmap(best["track"], best["missing"])

        confidence = self.confidence(results)

        alternatives = []
        for item in results[1:4]:
            alternatives.append({
                "track": item["track"],
                "match_score": item["score"],
                "matched_skills": item["matched"],
                "missing_skills": item["missing"],
                "explanation": self.explanation(item)
            })

        return {
            "recommended_track": best["track"],
            "skill_match_score": best["score"],
            "strength_analysis": strengths,
            "weakness_analysis": weaknesses,
            "missing_skills": best["missing"][:6],
            "mentor_recommendation": mentor,
            "confidence_score": confidence,
            "reasoning_summary": self.explanation(best),
            "roadmap": roadmap,
            "alternatives": alternatives
        }

    def best_mentor(self, track_name, matched):
        candidates = [m for m in self.mentors if m["track"] == track_name]
        if not candidates:
            return "Mentor assignment requires manual review."

        mentor = candidates[0]
        return mentor["name"]

    def strengths(self, item):
        if item["matched"]:
            return [
                f"Strong evidence for: {', '.join(item['matched'][:6])}.",
                f"{len(item['matched'])} relevant skills matched the recommended track.",
                "Profile content shows technical alignment with the selected internship."
            ]
        return ["Limited explicit skill evidence was found; mentor review is recommended."]

    def weaknesses(self, item):
        if item["missing"]:
            return [
                f"Missing or unverified skills: {', '.join(item['missing'][:6])}.",
                "Some track requirements are not yet demonstrated in the supplied profile."
            ]
        return ["No major missing skills detected from the supplied profile."]

    def explanation(self, item):
        matched = ", ".join(item["matched"][:5]) or "limited explicit skills"
        missing = ", ".join(item["missing"][:4]) or "none detected"
        return (
            f"Recommended because the profile matches {matched}. "
            f"Current match score is {item['score']}%. "
            f"Skills to strengthen or verify: {missing}."
        )

    def confidence(self, results):
        if len(results) < 2:
            return 50.0
        gap = max(0, results[0]["score"] - results[1]["score"])
        confidence = min(98, 55 + gap * 1.5)
        return round(confidence, 2)

    def make_roadmap(self, track, missing):
        base = {
            "AI / Machine Learning": [
                "Strengthen Python, NumPy and Pandas",
                "Learn supervised and unsupervised machine learning",
                "Build and evaluate 2 ML projects",
                "Learn model deployment with FastAPI/Streamlit",
                "Create a production-style AI project with documentation"
            ],
            "Data Science": [
                "Strengthen Python, Pandas and NumPy",
                "Practice statistics and exploratory data analysis",
                "Learn SQL for analytics",
                "Build dashboards and data storytelling projects",
                "Complete an end-to-end data science case study"
            ],
            "Web / Full Stack Development": [
                "Strengthen HTML, CSS and JavaScript",
                "Learn REST APIs and database integration",
                "Build a backend using FastAPI or Django",
                "Build a frontend using React",
                "Deploy a complete full-stack project"
            ],
            "Generative AI / LLM Engineering": [
                "Strengthen Python and NLP fundamentals",
                "Learn embeddings and vector databases",
                "Build a RAG pipeline",
                "Add evaluation, citations and hallucination controls",
                "Deploy an LLM application with monitoring"
            ],
            "AI Computer Vision": [
                "Strengthen Python and image processing",
                "Learn OpenCV",
                "Study CNN and transfer learning",
                "Build and evaluate a computer-vision project",
                "Deploy a real-time vision application"
            ]
        }
        roadmap = base.get(track, []).copy()
        if missing:
            roadmap.insert(0, "Priority gap: practice " + ", ".join(missing[:4]))
        return roadmap[:6]
