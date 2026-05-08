import os
import time
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="HackForge AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- API CONFIG ----------------
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #09090f 0%, #111827 50%, #1e1b4b 100%);
    color: white;
}
.main-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.card {
    padding: 22px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}
.agent-card {
    padding: 16px;
    border-radius: 15px;
    background: rgba(255,255,255,0.07);
    margin-bottom: 12px;
    border-left: 4px solid #38bdf8;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HELPERS ----------------
def run_agent(agent_name, role, user_data):
    prompt = f"""
You are {agent_name}, a specialized AI agent.

Role:
{role}

User hackathon requirements:
{json.dumps(user_data, indent=2)}

Generate detailed, practical, hackathon-ready output.
Use clear headings, bullets, and actionable suggestions.
Make it beginner-friendly but impressive.
"""

    response = model.generate_content(prompt)
    return response.text


def download_markdown(content):
    return content.encode("utf-8")


# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 HackForge AI")
st.sidebar.markdown("Multi-Agent Hackathon Builder")

st.sidebar.divider()

domain = st.sidebar.selectbox(
    "Choose Domain",
    ["AI/ML", "Healthcare", "Education", "FinTech", "Climate Tech", "Agriculture", "Cybersecurity", "Open Source", "Smart City"]
)

difficulty = st.sidebar.selectbox(
    "Difficulty Level",
    ["Beginner", "Intermediate", "Advanced"]
)

team_size = st.sidebar.slider("Team Size", 1, 6, 3)

tech_preference = st.sidebar.text_input(
    "Preferred Tech Stack",
    "Python, Streamlit, Gemini API, Google Cloud"
)

theme = st.sidebar.text_area(
    "Hackathon Theme / Problem Area",
    "Build an AI-powered solution that solves a real-world problem."
)

generate = st.sidebar.button("⚡ Generate Project", use_container_width=True)


# ---------------- MAIN UI ----------------
st.markdown('<h1 class="main-title">HackForge AI</h1>', unsafe_allow_html=True)
st.subheader("Multi-Agent AI Hackathon Builder")

st.markdown("""
<div class="card">
HackForge AI uses multiple AI agents to generate complete hackathon-ready projects:
idea, tech stack, architecture, README, pitch, UI plan, social posts, and deployment guide.
</div>
""", unsafe_allow_html=True)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='card'><h3>🤖 8 AI Agents</h3><p>Each agent handles a different project-building task.</p></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'><h3>⚡ Fast MVP</h3><p>Generate a full project plan in minutes.</p></div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'><h3>☁️ Cloud Ready</h3><p>Includes Docker + Google Cloud Run deployment guide.</p></div>", unsafe_allow_html=True)

st.write("")


# ---------------- AGENTS ----------------
agents = [
    {
        "name": "Idea Generator Agent",
        "role": "Generate a unique, innovative, practical hackathon project idea with problem statement, solution, target users, and impact."
    },
    {
        "name": "Tech Stack Architect Agent",
        "role": "Suggest the best frontend, backend, AI stack, database, APIs, and deployment tools."
    },
    {
        "name": "System Design Agent",
        "role": "Create architecture, workflow, folder structure, database design, and system modules."
    },
    {
        "name": "README Generator Agent",
        "role": "Generate a premium GitHub README with badges, features, setup, screenshots placeholder, deployment, and future scope."
    },
    {
        "name": "UI/UX Planner Agent",
        "role": "Suggest dashboard layout, colors, components, animations, and user experience flow."
    },
    {
        "name": "Pitch Deck Agent",
        "role": "Create hackathon pitch points, problem, solution, innovation, impact, tech stack, and future scope."
    },
    {
        "name": "Social Media Agent",
        "role": "Generate LinkedIn post, Devpost description, Twitter/X launch post, and hashtags."
    },
    {
        "name": "Deployment Agent",
        "role": "Generate Dockerfile explanation, requirements, environment setup, and Google Cloud Run deployment steps."
    }
]


if "final_output" not in st.session_state:
    st.session_state.final_output = ""

if generate:
    if not api_key:
        st.error("Please add GEMINI_API_KEY in your environment variables.")
    else:
        user_data = {
            "domain": domain,
            "difficulty": difficulty,
            "team_size": team_size,
            "tech_preference": tech_preference,
            "theme": theme
        }

        outputs = {}
        progress = st.progress(0)
        status = st.empty()

        for i, agent in enumerate(agents):
            status.info(f"Running {agent['name']}...")
            time.sleep(0.5)

            with st.expander(f"✅ {agent['name']}", expanded=True):
                result = run_agent(agent["name"], agent["role"], user_data)
                outputs[agent["name"]] = result
                st.markdown(result)

            progress.progress((i + 1) / len(agents))

        final_markdown = "# HackForge AI Generated Project\n\n"

        for agent_name, output in outputs.items():
            final_markdown += f"\n\n## {agent_name}\n\n{output}\n"

        st.session_state.final_output = final_markdown

        status.success("All agents completed successfully 🚀")


# ---------------- OUTPUT DOWNLOAD ----------------
if st.session_state.final_output:
    st.divider()
    st.subheader("📦 Export Generated Project Plan")

    st.download_button(
        label="Download Full Project Plan as Markdown",
        data=download_markdown(st.session_state.final_output),
        file_name="hackforge_ai_project_plan.md",
        mime="text/markdown"
    )

    st.subheader("📄 Full Generated Output")
    st.markdown(st.session_state.final_output)