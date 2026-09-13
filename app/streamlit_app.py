import streamlit as st
import sys
from pathlib import Path

# Project root ko path mein add karo
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.schemas import CandidateInput
from services.recommendation_engine import RecommendationEngine

st.set_page_config(
    page_title="EEF Match Engine",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

engine = RecommendationEngine()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none !important;}
    [data-testid="stSidebarCollapsedControl"] {display: none !important;}

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(160deg, #1C3334 0%, #2F4454 50%, #2E151B 100%);
        color: #e8d5dc;
        min-height: 100vh;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(16px) saturate(140%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(140%) !important;
        color: #f0e4e8 !important;
        border: 1.5px solid rgba(218, 123, 147, 0.35) !important;
        border-radius: 16px !important;
        font-size: 14px !important;
        padding: 14px 18px !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        transition: border-color 0.2s, box-shadow 0.2s, background 0.2s !important;
    }
    .stTextInput > div > div > input:hover,
    .stTextArea > div > div > textarea:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(218, 123, 147, 0.55) !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        background: rgba(255, 255, 255, 0.14) !important;
        border-color: #DA7B93 !important;
        box-shadow: 0 0 0 3px rgba(218, 123, 147, 0.25), 0 6px 28px rgba(0, 0, 0, 0.25) !important;
    }

    label {
        color: #DA7B93 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #DA7B93 0%, #376E6F 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 40px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 20px rgba(218, 123, 147, 0.35) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 8px 30px rgba(218, 123, 147, 0.5) !important;
        background: linear-gradient(135deg, #e895ab 0%, #DA7B93 50%, #376E6F 100%) !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(218, 123, 147, 0.25);
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetric"] label {
        color: #DA7B93 !important;
        font-size: 11px !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #fff !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    .card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(55, 110, 111, 0.35);
        border-radius: 18px;
        padding: 26px 28px;
        margin-bottom: 18px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.2);
    }
    .card h3 {
        margin: 0 0 14px 0;
        font-size: 12px;
        color: #DA7B93;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .hero-wrap { text-align: center; padding: 28px 0 40px 0; }
    .hero {
        font-size: 42px; font-weight: 800; color: #fff; margin-bottom: 8px;
        letter-spacing: -1px; text-shadow: 0 0 40px rgba(218, 123, 147, 0.25);
    }
    .hero span {
        background: linear-gradient(90deg, #DA7B93, #376E6F);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub { color: #8a9a9c; font-size: 15px; }

    .pill {
        display: inline-block; border-radius: 20px; padding: 6px 14px;
        margin: 4px 4px 4px 0; font-size: 13px; font-weight: 500;
    }
    .pill-ok {
        background: rgba(55, 110, 111, 0.25); color: #5eead4;
        border: 1px solid rgba(55, 110, 111, 0.5);
    }
    .pill-warn {
        background: rgba(251, 191, 36, 0.12); color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }
    .pill-err {
        background: rgba(218, 123, 147, 0.2); color: #DA7B93;
        border: 1px solid rgba(218, 123, 147, 0.4);
    }

    .step {
        background: rgba(0, 0, 0, 0.25); border-left: 3px solid #DA7B93;
        border-radius: 0 12px 12px 0; padding: 14px 18px; margin-bottom: 8px;
        color: #d0c0c6; font-size: 14px;
    }

    .empty {
        text-align: center; padding: 48px 24px;
        background: rgba(255, 255, 255, 0.06); backdrop-filter: blur(14px);
        border: 1.5px solid rgba(218, 123, 147, 0.3); border-radius: 20px;
    }
    .empty .icon { font-size: 48px; margin-bottom: 12px; }

    .section-title {
        font-size: 14px; font-weight: 700; color: #c4b0b8;
        letter-spacing: 0.5px; margin-bottom: 4px;
    }

    hr {
        border: none; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(218,123,147,0.4), transparent);
        margin: 28px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-wrap">
    <div class="hero">✦ EEF <span>Match Engine</span></div>
    <div class="sub">Internship track matching  ·  Mentor recommendation  ·  Skill roadmap</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-title">CANDIDATE DETAILS</p>', unsafe_allow_html=True)

row1 = st.columns(3)
with row1[0]:
    name = st.text_input("Name", "Student")
with row1[1]:
    education = st.text_input("Education", "BS Artificial Intelligence")
with row1[2]:
    github = st.text_input("GitHub (optional)", "")

row2 = st.columns(2)
with row2[0]:
    skills = st.text_area("Technical Skills", "Python, Machine Learning, Pandas, SQL", height=90)
    interests = st.text_area("Career Interests", "AI, Machine Learning, Generative AI", height=75)
with row2[1]:
    certifications = st.text_area("Certifications", "Python Certificate", height=75)
    portfolio = st.text_area("Portfolio / Projects", "Built machine learning and AI applications using Python.", height=90)

st.markdown("<br>", unsafe_allow_html=True)
btn_col = st.columns([1, 2, 1])
with btn_col[1]:
    generate = st.button("✦  Generate Recommendation")

st.markdown("---")

if generate:
    candidate = CandidateInput(
        name=name,
        education=education,
        skills=[x.strip() for x in skills.split(",") if x.strip()],
        interests=[x.strip() for x in interests.split(",") if x.strip()],
        certifications=[x.strip() for x in certifications.split(",") if x.strip()],
        portfolio_text=portfolio,
        github_username=github or None
    )
    try:
        with st.spinner("Matching tracks & building roadmap..."):
            result = engine.recommend(candidate)
            # Pydantic model → dict
            data = result.model_dump() if hasattr(result, "model_dump") else result.dict()

        m1, m2, m3 = st.columns(3)
        m1.metric("Recommended Track", data["recommended_track"])
        m2.metric("Skill Match", f"{data['skill_match_score']}%")
        m3.metric("Confidence", f"{data['confidence_score']}%")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f'<div class="card"><h3>AI Reasoning</h3><p style="color:#b0a0a8;line-height:1.7;margin:0;font-size:14px;">{data["reasoning_summary"]}</p></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            strengths = "".join(f'<span class="pill pill-ok">{i}</span>' for i in data["strength_analysis"]) or '<span style="color:#6b7280">None</span>'
            st.markdown(f'<div class="card"><h3>Strengths</h3>{strengths}</div>', unsafe_allow_html=True)
        with col2:
            weaknesses = "".join(f'<span class="pill pill-warn">{i}</span>' for i in data["weakness_analysis"]) or '<span style="color:#6b7280">None</span>'
            st.markdown(f'<div class="card"><h3>Weaknesses</h3>{weaknesses}</div>', unsafe_allow_html=True)

        missing = "".join(f'<span class="pill pill-err">{s}</span>' for s in data["missing_skills"]) or '<span style="color:#5eead4">No major gaps</span>'
        st.markdown(f'<div class="card"><h3>Missing Skills</h3>{missing}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="card"><h3>Recommended Mentor</h3><p style="color:#fff;font-size:18px;margin:0;font-weight:600;">{data["mentor_recommendation"]}</p></div>', unsafe_allow_html=True)

        steps = "".join(f'<div class="step"><b>Step {i}</b> — {s}</div>' for i, s in enumerate(data["roadmap"], 1))
        st.markdown(f'<div class="card"><h3>Learning Roadmap</h3>{steps}</div>', unsafe_allow_html=True)

        st.markdown('<p class="section-title">ALTERNATIVE TRACKS</p>', unsafe_allow_html=True)
        for item in data["alternatives"]:
            with st.expander(f"**{item['track']}**  ·  {item['match_score']}%"):
                st.write(item["explanation"])
                st.markdown("**Matched:** " + (", ".join(item["matched_skills"]) or "None"))
                st.markdown("**Missing:** " + (", ".join(item["missing_skills"]) or "None"))

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.markdown("""
    <div class="empty">
        <div class="icon">✦</div>
        <p style="color:#8a9a9c;margin:0;font-size:15px;">
            Fill the form above and click
            <b style="color:#DA7B93;">Generate Recommendation</b>
        </p>
    </div>
    """, unsafe_allow_html=True)