"""
GrandPa's Gyan - Master Streamlit Orchestrator App (V2 Core Operating System)
Integrates All 25 Specialist Agents, RAG Engine, Persistent Memory, PDF, Vision, Voice, AST Calculator & Verification.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

st.set_page_config(
    page_title="GrandPa's Gyan V2 Core OS",
    page_icon="🧓",
    layout="wide"
)

from config import get_api_key
from agents_registry import AGENTS_DATABASE
from agent_router import route_agent_automatically, get_agent_config
from gemini_service import stream_gemini_response, get_client
from rag_engine import retrieve_curriculum_context
from memory.student_memory import (
    init_db, log_activity, get_student_stats, get_profile, update_profile,
    log_mistake, get_mistakes, save_bookmark, get_bookmarks, record_quiz_score
)
from curriculum import get_boards, get_grades, get_subjects, get_chapters, get_topics
from tools.pdf import process_pdf_document
from tools.vision import process_image
from tools.voice import text_to_speech
from tools.mindmap import generate_mindmap_markdown
from tools.verification import verify_math_calculation
from tools.exam import generate_exam_analysis_prompt

# Initialize SQLite Schema
init_db()

# Validate API Key
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
if "enable_tts" not in st.session_state:
    st.session_state.enable_tts = True

profile = get_profile()

# Sidebar Orchestration
st.sidebar.title("🧓 GrandPa's Gyan V2")
st.sidebar.caption(f"Student: **{profile['name']}** | {profile['grade']} ({profile['board']})")

nav_page = st.sidebar.radio(
    "Navigation", 
    ["💬 Workspace", "📚 Curriculum & RAG", "📄 Previous Paper Analyzer", "❌ Mistake Notebook", "⭐ Bookmarks & Library", "📊 Student Progress", "⚙️ Profile & Settings"]
)

# --- NAVIGATION 1: CURRICULUM BROWSER & RAG ---
if nav_page == "📚 Curriculum & RAG":
    st.title("📚 Curriculum Browser & RAG Knowledge Engine")
    c1, c2, c3 = st.columns(3)

    board = c1.selectbox("Board", get_boards())
    grade = c2.selectbox("Grade", get_grades(board))
    subject = c3.selectbox("Subject", get_subjects(board, grade))

    chapters = get_chapters(board, grade, subject)
    if chapters:
        selected_ch = st.selectbox("Select Chapter", chapters)
        topics = get_topics(board, grade, subject, selected_ch)

        st.subheader(f"Chapter: {selected_ch}")
        for t in topics:
            st.markdown(f"* {t}")

        st.markdown("---")
        st.subheader("🔍 NCERT / CBSE Context Retriever")
        search_q = st.text_input("Search NCERT Knowledge Base:", value=selected_ch)
        if search_q:
            context = retrieve_curriculum_context(search_q, grade, subject)
            st.info(f"**Retrieved Curriculum Snippet:**\n\n{context}")
    st.stop()

# --- NAVIGATION 2: PREVIOUS PAPER ANALYZER ---
if nav_page == "📄 Previous Paper Analyzer":
    st.title("📄 Previous Year Question Paper Analyzer")
    subj_paper = st.selectbox("Paper Subject", ["Mathematics", "Physics", "Chemistry", "Biology", "English", "General"])
    uploaded_paper = st.file_uploader("Upload Question Paper (PDF)", type=["pdf"])

    if uploaded_paper and st.button("🔍 Analyze Paper Trends"):
        doc_text, file_obj = process_pdf_document(uploaded_paper, client=get_client())
        if doc_text or file_obj:
            analysis_prompt = generate_exam_analysis_prompt(doc_text if doc_text else "Attached PDF Document", subj_paper)
            with st.spinner("GrandPa is analyzing paper weightage & key topics..."):
                gen = stream_gemini_response(
                    system_instruction="You are an expert exam paper trend analyst.",
                    user_prompt=analysis_prompt,
                    file_doc=file_obj
                )
                st.write_stream(gen)
        else:
            st.error("Could not process uploaded document.")
    st.stop()

# --- NAVIGATION 3: MISTAKE NOTEBOOK ---
if nav_page == "❌ Mistake Notebook":
    st.title("❌ Mistake Notebook & Targeted Practice")
    mistakes = get_mistakes()
    if mistakes:
        for idx, m in enumerate(mistakes, 1):
            with st.expander(f"Mistake #{idx}: {m['subject']} - {m['concept']}"):
                st.write(f"**Question:** {m['question']}")
                st.write(f"**Your Answer:** {m['user_answer']}")
                st.write(f"**Correct Answer:** {m['correct_answer']}")
    else:
        st.success("No past mistakes logged. Keep up the great work!")

    with st.form("add_mistake_form"):
        st.subheader("Log a New Misconception")
        m_subj = st.selectbox("Subject", ["Mathematics", "Science", "Physics", "Chemistry", "Biology", "English", "General"])
        m_q = st.text_input("Question / Concept")
        m_u_ans = st.text_input("What you answered incorrectly")
        m_c_ans = st.text_input("Correct Answer")
        m_concept = st.text_input("Core Concept to Revise")
        if st.form_submit_button("Save Mistake"):
            log_mistake(m_subj, m_q, m_u_ans, m_c_ans, m_concept)
            st.success("Mistake logged successfully.")
    st.stop()

# --- NAVIGATION 4: BOOKMARKS & LIBRARY ---
if nav_page == "⭐ Bookmarks & Library":
    st.title("⭐ Saved Library & Bookmarks")
    bks = get_bookmarks()
    if bks:
        for b in bks:
            with st.expander(f"📌 [{b['category']}] {b['title']}"):
                st.markdown(b['content'])
    else:
        st.info("No bookmarks saved yet. Use the 'Save Answer' button in the workspace.")
    st.stop()

# --- NAVIGATION 5: STUDENT PROGRESS ---
if nav_page == "📊 Student Progress":
    st.title("📊 Adaptive Progress & Mastery Dashboard")
    stats = get_student_stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("🔥 Study Streak", f"{stats['streak_days']} Days")
    c2.metric("💬 Total Questions", stats['total_interactions'])
    c3.metric("🎯 Weak Area Focus", stats['weakest_subject'])

    st.markdown("---")
    st.subheader("Subject Mastery & Difficulty Calibration")
    for subj, score in stats['scores'].items():
        lvl = stats['levels'].get(subj, "Medium")
        col_a, col_b = st.columns([3, 1])
        col_a.write(f"**{subj}** (Mastery: {score}%)")
        col_a.progress(min(int(score), 100))
        col_b.info(f"Target Level: **{lvl}**")
    st.stop()

# --- NAVIGATION 6: PROFILE & SETTINGS ---
if nav_page == "⚙️ Profile & Settings":
    st.title("⚙️ Profile & System Settings")
    with st.form("profile_form"):
        u_name = st.text_input("Student Name", value=profile["name"])
        u_board = st.selectbox("Education Board", get_boards())
        u_grade = st.selectbox("Grade", ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"])
        u_lang = st.selectbox("Explanation Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Marathi"])
        u_font = st.selectbox("Font Size", ["Standard", "Large"])
        if st.form_submit_button("Save Profile Settings"):
            update_profile(u_name, u_board, u_grade, u_lang, u_font)
            st.success("Profile saved successfully!")
    st.stop()

# --- NAVIGATION 7: WORKSPACE ---
st.sidebar.markdown("---")
st.session_state.auto_route = st.sidebar.checkbox("⚡ Auto-Route Intent Router", value=True)
st.session_state.enable_tts = st.sidebar.checkbox("🔊 Enable GrandPa Voice (TTS)", value=True)

cat_filter = st.sidebar.selectbox("📂 Category", ["All"] + sorted(list(set(a["category"] for a in AGENTS_DATABASE.values()))))

filtered_agents = [
    name for name, details in AGENTS_DATABASE.items()
    if cat_filter == "All" or details["category"] == cat_filter
]

selected_agent_name = st.sidebar.radio(
    "Active Specialist Agent:",
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
        if "audio" in msg:
            st.audio(msg["audio"], format="audio/mp3")

with st.expander("📎 Attach Documents or Images (Optional)"):
    c1, c2 = st.columns(2)
    with c1:
        uploaded_pdf = st.file_uploader("Upload Document (PDF)", type=["pdf"], key=f"pdf_{selected_agent_name}")
    with c2:
        uploaded_image = st.file_uploader("Upload Image / Homework Problem", type=["png", "jpg", "jpeg"], key=f"img_{selected_agent_name}")

user_input = st.chat_input("Ask GrandPa...")

if user_input:
    target_agent_name = route_agent_automatically(user_input, selected_agent_name) if st.session_state.auto_route else selected_agent_name
    active_agent = get_agent_config(target_agent_name)

    if target_agent_name != selected_agent_name:
        st.info(f"⚡ Intent Router assigned query to **{active_agent['icon']} {target_agent_name}**")

    st.session_state.chat_history[selected_agent_name].append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    attachments, doc_text, file_obj = [], None, None

    if uploaded_pdf:
        doc_text, file_obj = process_pdf_document(uploaded_pdf, client=get_client())

    if uploaded_image:
        img_obj = process_image(uploaded_image)
        if img_obj:
            attachments.append(img_obj)

    # Context and Adaptive Level Retrieval
    rag_context = retrieve_curriculum_context(user_input, profile["grade"], "Science")
    stats = get_student_stats()
    subj_key = target_agent_name.split()[0]
    target_level = stats['levels'].get(subj_key, "Medium")

    system_instruction = (
        f"{active_agent['instruction']}\n"
        f"Student Profile: Grade {profile['grade']}, Board {profile['board']}.\n"
        f"Target Difficulty Level: {target_level}.\n"
        f"Target Language: {profile['language']}.\n"
        f"NCERT Context: {rag_context}"
    )

    prompt_payload = user_input
    if doc_text:
        prompt_payload = f"--- DOCUMENT TEXT ---\n{doc_text}\n\n--- QUESTION ---\n{user_input}"

    log_activity(target_agent_name)

    with st.chat_message("assistant"):
        if target_agent_name == "Mind Map Generator":
            full_response = generate_mindmap_markdown(user_input)
            st.markdown(full_response)
        else:
            response_gen = stream_gemini_response(
                system_instruction=system_instruction,
                user_prompt=prompt_payload,
                attachments=attachments,
                file_doc=file_obj,
                tools_list=active_agent.get("tools", [])
            )
            full_response = st.write_stream(response_gen)

            # Verification Engine Pass
            verification_notice = verify_math_calculation(full_response)
            if verification_notice:
                st.markdown(verification_notice)
                full_response += verification_notice

        # TTS Synthesis
        audio_stream = None
        if st.session_state.enable_tts:
            try:
                audio_stream = text_to_speech(full_response, lang_code=profile['language'])
                st.audio(audio_stream, format="audio/mp3", autoplay=True)
            except Exception as voice_err:
                st.caption(f"🔊 Audio unavailable: {str(voice_err)}")

        if st.button("⭐ Save Answer to Bookmarks", key=f"bk_{len(st.session_state.chat_history[selected_agent_name])}"):
            save_bookmark(title=user_input[:30], content=full_response, category=target_agent_name)
            st.success("Saved to Bookmarks!")

    assistant_entry = {"role": "assistant", "content": full_response}
    if audio_stream:
        assistant_entry["audio"] = audio_stream

    st.session_state.chat_history[selected_agent_name].append(assistant_entry)
