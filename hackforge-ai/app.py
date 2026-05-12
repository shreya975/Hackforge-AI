import time
import json
import requests
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="HackForge AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #050816 0%,
        #0f172a 45%,
        #1e1b4b 100%
    );
    color: white;
}

.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(
        90deg,
        #38bdf8,
        #8b5cf6,
        #f472b6
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card {
    padding: 22px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
    border: none;
    font-weight: bold;
    color: white;
    background: linear-gradient(
        90deg,
        #38bdf8,
        #8b5cf6
    );
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- CHECK OLLAMA ----------------
def check_ollama():
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    except:
        return False

# ---------------- AI AGENT ----------------
def run_agent(agent_name, role, user_data):

    prompt = f"""
You are {agent_name}.

Role:
{role}

User Requirements:
{json.dumps(user_data, indent=2)}

Give short concise output.
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            },
            timeout=1000
        )

        data = response.json()

        return data.get(
            "response",
            "No response generated."
        )

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- DOWNLOAD ----------------
def download_markdown(content):
    return content.encode("utf-8")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 HackForge AI")
st.sidebar.markdown("Multi-Agent Hackathon Builder")

st.sidebar.divider()

domain = st.sidebar.selectbox(
    "Choose Domain",
    [
        "AI/ML",
        "Healthcare",
        "Education",
        "FinTech",
        "Agriculture",
        "Cybersecurity",
        "Open Source"
    ]
)

difficulty = st.sidebar.selectbox(
    "Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

team_size = st.sidebar.slider(
    "Team Size",
    1,
    6,
    3
)

tech_preference = st.sidebar.text_input(
    "Preferred Tech Stack",
    "Python, Streamlit, Ollama, Phi3"
)

theme = st.sidebar.text_area(
    "Hackathon Theme / Problem Area",
    "Build an AI-powered solution that solves a real-world problem."
)

generate = st.sidebar.button(
    "⚡ Generate Project"
)

# ---------------- MAIN TITLE ----------------
st.markdown(
    '<h1 class="main-title">HackForge AI</h1>',
    unsafe_allow_html=True
)

st.subheader("Multi-Agent AI Hackathon Builder")

st.markdown("""
<div class="card">
HackForge AI uses multiple AI agents to generate:
project ideas, README files, tech stack suggestions,
deployment guides, and hackathon content automatically.
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- FEATURE CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>🤖 AI Agents</h3>
    <p>Multiple AI agents collaborate together.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>⚡ Fast MVP</h3>
    <p>Generate hackathon-ready projects quickly.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>☁️ Cloud Ready</h3>
    <p>Deployment-ready architecture suggestions.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- LIGHTWEIGHT AGENTS ----------------
agents = [

    {
        "name": "Idea Generator Agent",
        "role": "Generate innovative hackathon project ideas with features and users."
    },

    {
        "name": "Tech Stack Agent",
        "role": "Suggest frontend, backend, APIs, AI tools, and deployment stack."
    },

    {
        "name": "README Agent",
        "role": "Generate a professional GitHub README structure."
    }

]

# ---------------- SESSION STATE ----------------
if "final_output" not in st.session_state:
    st.session_state.final_output = ""

# ---------------- GENERATE ----------------
if generate:

    if not check_ollama():

        st.error("""
❌ Ollama is not running.

Open terminal and run:

ollama run phi3
""")

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

            status.info(
                f"Running {agent['name']}..."
            )

            with st.expander(
                f"✅ {agent['name']}",
                expanded=True
            ):

                result = run_agent(
                    agent["name"],
                    agent["role"],
                    user_data
                )

                outputs[agent["name"]] = result

                st.markdown(result)

            progress.progress(
                (i + 1) / len(agents)
            )

            time.sleep(1)

        final_markdown = "# 🚀 HackForge AI Output\n\n"

        for agent_name, output in outputs.items():

            final_markdown += f"""
## {agent_name}

{output}

"""

        st.session_state.final_output = final_markdown

        status.success(
            "All AI agents completed successfully 🚀"
        )

# ---------------- DOWNLOAD SECTION ----------------
if st.session_state.final_output:

    st.divider()

    st.subheader("📦 Export Generated Output")

    st.download_button(
        label="Download Markdown File",
        data=download_markdown(
            st.session_state.final_output
        ),
        file_name="hackforge_output.md",
        mime="text/markdown"
    )

    st.subheader("📄 Final Generated Output")

    st.markdown(
        st.session_state.final_output
    )