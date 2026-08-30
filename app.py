"""
GrandPa's Gyan - AI Educational Platform
Main Streamlit Application with 24x7 Autopilot Sentinel
"""

import sys
import os

# Fix Streamlit Cloud Module Resolution Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# Initialize Streamlit Page Configuration First
st.set_page_config(
    page_title="GrandPa's Gyan",
    page_icon="🧓",
    layout="wide"
)

# Run 24x7 Autopilot Security & Maintenance Sentinel on Load
try:
    from tools.autopilot import run_autopilot_sentinel
    autopilot_report = run_autopilot_sentinel()
except Exception as e:
    autopilot_report = {"Autopilot Engine": f"Initialization Warning: {str(e)}"}

# Local Core Modules
from config import get_api_key
from agents_registry import AGENTS_DATABASE
from agent_router import route_agent_automatically, get_agent_config
from gemini_service import stream_gemini_response, get_client
from memory.student_memory import (
    init_db, log_activity, get_student_stats, get_profile, update_profile, record_quiz_score
)
from curriculum import get_boards, get_grades, get_subjects, get_chapters, get_topics
from tools.pdf import process_pdf_document
from tools.vision import process_image
from tools.voice import text_to_speech
from tools.exam import generate_exam_analysis_prompt

# Initialize SQLite Database Schema
init_db()

# API Key Validation
api_key = get_api_key()
if not api_key:
    api_key_input = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")
    if not api_key_input:
        st.info("⚠️ Please enter your Gemini API Key in the sidebar or Streamlit Secrets to launch GrandPa's Gyan.")
        st.stop()
    st.secrets["GEMINI_API_KEY"] = api_key_input

# Session State Setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "auto_route" not in st.session_state:
    st.session_state.auto_route = True

profile = get_profile()

# Sidebar Navigation & System Diagnostics Expander
st.sidebar.title("🧓 GrandPa's Gyan")
st.sidebar.caption(f"Student: **{profile['name']}** | {profile['grade']} ({profile['board']})")

with st.sidebar.expander("🛡️ Autopilot Security & System Health"):
    for check, status in autopilot_report.items():
        st.caption(f"**{check.replace('_', ' ').title()}**: `{status}`")

nav_page = st.sidebar.radio(
    "Navigation", 
    ["💬 Workspace", "📚 Curriculum Browser", "📝 Previous Paper Analyzer", "📊 Student Progress", "⚙️ Profile & Settings"]
)

# --- PAGE 1: CURRICULUM BROWSER ---
if nav_page == "📚 Curriculum Browser":
    st.title("📚 Curriculum Hierarchy Browser")
    c1, c2, c3 = st.columns(3)
    
    board = c1.selectbox("Board", get_boards())
    grade = c2.selectbox("Grade", get_grades(board))
    subject = c3.selectbox("Subject", get_subjects(board, grade))
    
    chapters = get_chapters(board, grade, subject)
    if chapters:
        selected_ch = st.selectbox("Select Chapter", chapters)
        topics = get_topics(board, grade, subject, selected_ch)
        
        st.subheader(f"Chapter: {selected_ch}")
        st.markdown("**Topics Covered:**")
        for t in topics:
            st.markdown(f"* {t}")
            
        if st.button("🚀 Practice This Chapter with GrandPa"):
            st.session_state.active_chapter_prompt = f"Explain the key concepts of {selected_ch} in {subject} for {grade} ({board})."
            st.success("Context loaded! Switch to 💬 Workspace to start learning.")
    else:
        st.info("No chapter data available for this selection.")
    st.stop()

# --- PAGE 2: PREVIOUS PAPER ANALYZER ---
if nav_page == "📝 Previous Paper Analyzer":
    st.title("📝 Previous Year Paper Analyzer")
    st.caption("Upload exam papers to extract high-frequency topics and question trends.")
    
    subj_name = st.selectbox("Subject", ["Mathematics", "Physics", "Chemistry", "Biology", "General"])
    uploaded_paper = st.file_uploader("Upload Question Paper (PDF)", type=["pdf"])
    
    if uploaded_paper and st.button("🔍 Analyze Exam Trends"):
        doc_text, file_obj = process_pdf_document(uploaded_paper, client=get_client())
        if doc_text or file_obj:
            analysis_prompt = generate_exam_analysis_prompt(doc_text if doc_text else "Attached Document", subj_name)
            
            with st.spinner("GrandPa is analyzing paper patterns..."):
                gen = stream_gemini_response(
                    system_instruction="You are an expert exam paper trend analyst.",
                    user_prompt=analysis_prompt,
                    file_doc=file_obj
                )
                st.write_stream(gen)
        else:
            st.error("Failed to extract text from the paper.")
    st.stop()

# --- PAGE 3: STUDENT PROGRESS ---
if nav_page == "📊 Student Progress":
    st.title("📊 Adaptive Learning & Progress Dashboard")
    stats = get_student_stats()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Study Streak", f"{stats['streak_days']} Days")
    col2.metric("💬 Questions Asked", stats['total_interactions'])
    col3.metric("🎯 Weakest Subject", stats['weakest_subject'])
    
    st.markdown("---")
    st.subheader("Subject Mastery & Adaptive Difficulty Levels")
    
    for subj, score in stats['scores'].items():
        lvl = stats['levels'].get(subj, "Medium")
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{subj}** (Mastery: {score}%)")
        c1.progress(min(int(score), 100))
        c2.info(f"Target: **{lvl}**")
        
    st.stop()

# --- PAGE 4: PROFILE & SETTINGS ---
if nav_page == "⚙️ Profile & Settings":
    st.title("⚙️ Student Profile & Settings")
    
    with st.form("profile_form"):
        u_name = st.text_input("Student Name", value=profile["name"])
        u_board = st.selectbox("Education Board", get_boards(), index=0)
        u_grade = st.selectbox("Grade Level", ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"], index=4)
        u_lang = st.selectbox("Preferred Explanation Language", ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Marathi"])
        u_font = st.selectbox("UI Font Size", ["Standard", "Large"])
        
        if st.form_submit_button("Save Profile"):
            update_profile(u_name, u_board, u_grade, u_lang, u_font)
            st.success("Profile updated successfully!")
    st.stop()

# --- WORKSPACE PAGE ---
st.sidebar.markdown("---")
st.session_state.auto_route = st.sidebar.checkbox("⚡ Auto-Route Questions to Agents", value=True)

cat_filter = st.sidebar.selectbox("📂 Category", ["All"] + sorted(list(set(a["category"] for a in AGENTS_DATABASE.values()))))

filtered_agents = [
    name for name, details in AGENTS_DATABASE.items()
    if cat_filter == "All" or details["category"] == cat_filter
]

selected_agent_name = st.sidebar.radio(
    "Active UI Agent:",
    filtered_agents,
    format_func=lambda x: f"{AGENTS_DATABASE[x]['icon']} {x}"
)

ui_agent_config = get_agent_config(selected_agent_name)
st.title(f"{ui_agent_config['icon']} {selected_agent_name}")
st.caption(f"{ui_agent_config['description']} | Language: **{profile['language']}**")

if selected_agent_name not in st.session_state.chat_history:
    st.session_state.chat_history[selected_agent_name] = []

for msg in st.session_state.chat_history[selected_agent_name]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

with st.expander("📎 Attach Documents or Images (Optional)"):
    c1, c2 = st.columns(2)
    with c1:
        uploaded_pdf = st.file_uploader("Upload Document (PDF)", type=["pdf"], key=f"pdf_{selected_agent_name}")
    with c2:
        uploaded_image = st.file_uploader("Upload Image / Problem", type=["png", "jpg", "jpeg"], key=f"img_{selected_agent_name}")

initial_input = getattr(st.session_state, "active_chapter_prompt", None)
if initial_input:
    del st.session_state.active_chapter_prompt

user_input = st.chat_input("Ask GrandPa...") or initial_input

if user_input:
    target_agent_name = route_agent_automatically(user_input, selected_agent_name) if st.session_state.auto_route else selected_agent_name
    active_agent = get_agent_config(target_agent_name)
    
    if target_agent_name != selected_agent_name:
        st.info(f"⚡ Auto-routed question to **{active_agent['icon']} {target_agent_name}**")

    st.session_state.chat_history[selected_agent_name].append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    attachments, doc_text, file_obj = [], None, None

    if uploaded_pdf:
        doc_text, file_obj = process_pdf_document(uploaded_pdf, client=get_client())
        if doc_text:
            st.info(f"📄 Loaded PDF text context ({len(doc_text)} chars)")

    if uploaded_image:
        img_obj = process_image(uploaded_image)
        if img_obj:
            attachments.append(img_obj)
            st.image(img_obj, caption="Attached Visual Focus", width=250)

    # Adaptive Instruction Construction
    stats = get_student_stats()
    subj_key = target_agent_name.split()[0]
    target_level = stats['levels'].get(subj_key, "Medium")
    
    system_instruction = (
        f"{active_agent['instruction']}\n"
        f"Student Profile: Grade {profile['grade']}, Board {profile['board']}.\n"
        f"Target Difficulty Level: {target_level}.\n"
        f"Respond in {profile['language']} language where applicable."
    )

    prompt_payload = user_input
    if doc_text:
        prompt_payload = f"--- DOCUMENT CONTEXT ---\n{doc_text}\n\n--- INQUIRY ---\n{user_input}"

    log_activity(target_agent_name)

    with st.chat_message("assistant"):
        response_gen = stream_gemini_response(
            system_instruction=system_instruction,
            user_prompt=prompt_payload,
            attachments=attachments,
            file_doc=file_obj,
            tools_list=active_agent.get("tools", [])
        )
        
        full_response = st.write_stream(response_gen)

        if "voice_engine" in active_agent.get("tools", []):
            try:
                audio_fp = text_to_speech(full_response)
                st.audio(audio_fp, format="audio/mp3")
            except Exception:
                pass

    st.session_state.chat_history[selected_agent_name].append({"role": "assistant", "content": full_response})
