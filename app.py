"""
GrandPa's Gyan - AI Educational Workspace
"""

import streamlit as st

st.set_page_config(
    page_title="GrandPa's Gyan",
    page_icon="🧓",
    layout="wide"
)

from config import get_api_key
from agents_registry import AGENTS_DATABASE
from agent_router import route_agent_automatically, get_agent_config
from gemini_service import stream_gemini_response, get_client
from memory.student_memory import init_db, log_activity, get_student_stats
from tools.pdf import process_pdf_document
from tools.vision import process_image

# Initialize DB
init_db()

# API Key Validation
api_key = get_api_key()
if not api_key:
    api_key_input = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")
    if not api_key_input:
        st.info("⚠️ Please provide a valid Gemini API Key to continue.")
        st.stop()
    st.secrets["GEMINI_API_KEY"] = api_key_input

# State Setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "auto_route" not in st.session_state:
    st.session_state.auto_route = True

# Navigation
st.sidebar.title("🧓 GrandPa's Gyan")
nav_page = st.sidebar.radio("Navigation", ["💬 Workspace", "📊 Student Dashboard"])

if nav_page == "📊 Student Dashboard":
    st.title("📊 Student Progress Dashboard")
    stats = get_student_stats()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("🔥 Study Streak", f"{stats['streak_days']} Days")
    c2.metric("💬 Total Questions", stats['total_interactions'])
    c3.metric("🎯 Subject Focus", stats['weakest_subject'])
    
    st.markdown("---")
    st.subheader("Subject Mastery")
    for subj, score in stats['scores'].items():
        st.write(f"**{subj}**: {score}%")
        st.progress(min(int(score), 100))
    st.stop()

# Workspace setup
st.sidebar.markdown("---")
st.session_state.auto_route = st.sidebar.checkbox("⚡ Auto-Route Queries", value=True)

categories = ["All"] + sorted(list(set(a["category"] for a in AGENTS_DATABASE.values())))
selected_cat = st.sidebar.selectbox("📂 Category", categories)

filtered_agents = [
    name for name, details in AGENTS_DATABASE.items()
    if selected_cat == "All" or details["category"] == selected_cat
]

selected_agent = st.sidebar.radio(
    "Active UI Agent:",
    filtered_agents,
    format_func=lambda x: f"{AGENTS_DATABASE[x]['icon']} {x}"
)

agent_cfg = get_agent_config(selected_agent)
st.title(f"{agent_cfg['icon']} {selected_agent}")
st.caption(agent_cfg["description"])

if selected_agent not in st.session_state.chat_history:
    st.session_state.chat_history[selected_agent] = []

for msg in st.session_state.chat_history[selected_agent]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask GrandPa...")

if user_input:
    target_agent = route_agent_automatically(user_input, selected_agent) if st.session_state.auto_route else selected_agent
    active_cfg = get_agent_config(target_agent)
    
    if target_agent != selected_agent:
        st.info(f"⚡ Auto-routed to **{active_cfg['icon']} {target_agent}**")

    st.session_state.chat_history[selected_agent].append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    log_activity(target_agent)

    with st.chat_message("assistant"):
        response_gen = stream_gemini_response(
            system_instruction=active_cfg["instruction"],
            user_prompt=user_input,
            tools_list=active_cfg.get("tools", [])
        )
        full_resp = st.write_stream(response_gen)

    st.session_state.chat_history[selected_agent].append({"role": "assistant", "content": full_resp})
