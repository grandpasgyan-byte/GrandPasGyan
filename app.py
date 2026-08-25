"""
GrandPa's Gyan - AI Educational Workspace
Main Streamlit application managing page routing, state, uploads, and AI integration.
"""

import streamlit as st

# Setup Page Configuration
st.set_page_config(
    page_title="GrandPa's Gyan",
    page_icon="🧓",
    layout="wide"
)

# Import Local Modules
from config import get_api_key
from agents_registry import AGENTS_DATABASE
from agent_router import route_agent_automatically, get_agent_config
from gemini_service import stream_gemini_response, get_client
from memory.student_memory import init_db, log_activity, get_student_stats
from tools.pdf import process_pdf_document
from tools.vision import process_image

# Initialize Database Storage
init_db()

# Validate Gemini API Credentials
api_key = get_api_key()
if not api_key:
    api_key_input = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")
    if not api_key_input:
        st.info("⚠️ Please enter your Gemini API Key in the sidebar or setup Streamlit Secrets to launch GrandPa's Gyan.")
        st.stop()
    st.secrets["GEMINI_API_KEY"] = api_key_input

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "auto_route" not in st.session_state:
    st.session_state.auto_route = True

# App Navigation
st.sidebar.title("🧓 GrandPa's Gyan")
nav_page = st.sidebar.radio("Navigation", ["💬 Workspace", "📊 Student Dashboard"])

if nav_page == "📊 Student Dashboard":
    st.title("📊 Student Progress Dashboard")
    st.caption("Track your learning stats, streaks, and subject mastery.")
    
    stats = get_student_stats()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Study Streak", f"{stats['streak_days']} Days")
    col2.metric("💬 Total Questions Asked", stats['total_interactions'])
    col3.metric("🎯 Subject to Practice", stats['weakest_subject'])
    
    st.markdown("---")
    st.subheader("Subject Mastery Levels")
    
    for subject, score in stats['scores'].items():
        st.write(f"**{subject}**: {score}%")
        st.progress(min(int(score), 100))
        
    st.stop()

# --- WORKSPACE PAGE ---
st.sidebar.markdown("---")
st.session_state.auto_route = st.sidebar.checkbox("⚡ Auto-Route Questions to Relevant Agent", value=True)

# Agent Category Filtering
category_filter = st.sidebar.selectbox(
    "📂 Category Filter", 
    ["All"] + sorted(list(set(a["category"] for a in AGENTS_DATABASE.values())))
)

filtered_agents = [
    name for name, details in AGENTS_DATABASE.items()
    if category_filter == "All" or details["category"] == category_filter
]

selected_agent_name = st.sidebar.radio(
    "Active UI Agent:",
    filtered_agents,
    format_func=lambda x: f"{AGENTS_DATABASE[x]['icon']} {x}"
)

# Active Agent Setup
ui_agent_config = get_agent_config(selected_agent_name)
st.title(f"{ui_agent_config['icon']} {selected_agent_name}")
st.caption(ui_agent_config["description"])

if selected_agent_name not in st.session_state.chat_history:
    st.session_state.chat_history[selected_agent_name] = []

# Display Current Agent Chat History
for msg in st.session_state.chat_history[selected_agent_name]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Multi-Modal Upload Controls
with st.expander("📎 Attach Documents or Images (Optional)"):
    c1, c2 = st.columns(2)
    with c1:
        uploaded_pdf = st.file_uploader("Upload PDF Document", type=["pdf"], key=f"pdf_{selected_agent_name}")
    with c2:
        uploaded_image = st.file_uploader("Upload Image / Homework", type=["png", "jpg", "jpeg"], key=f"img_{selected_agent_name}")

# User Input Execution
user_input = st.chat_input(f"Ask GrandPa...")

if user_input:
    # Auto-Route Intent Detection
    if st.session_state.auto_route:
        target_agent_name = route_agent_automatically(user_input, selected_agent_name)
    else:
        target_agent_name = selected_agent_name
        
    active_agent = get_agent_config(target_agent_name)
    
    if target_agent_name != selected_agent_name:
        st.info(f"⚡ Auto-routed question to **{active_agent['icon']} {target_agent_name}**")

    # Render User Message
    st.session_state.chat_history[selected_agent_name].append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Process Attachments
    attachments = []
    doc_text = None
    file_obj = None

    if uploaded_pdf:
        client_instance = get_client()
        doc_text, file_obj = process_pdf_document(uploaded_pdf, client=client_instance)
        if doc_text:
            st.info(f"📄 Loaded PDF context ({len(doc_text)} chars)")
        elif file_obj:
            st.info("📄 File uploaded to Gemini File API for indexing.")

    if uploaded_image:
        img_obj = process_image(uploaded_image)
        if img_obj:
            attachments.append(img_obj)
            st.image(img_obj, caption="Attached Homework Image", width=250)

    # Construct Final Prompt
    prompt_payload = user_input
    if doc_text:
        prompt_payload = f"--- DOCUMENT CONTEXT ---\n{doc_text}\n\n--- USER INQUIRY ---\n{user_input}"

    # Log Student Activity
    log_activity(target_agent_name)

    # Stream AI Response
    with st.chat_message("assistant"):
        response_gen = stream_gemini_response(
            system_instruction=active_agent["instruction"],
            user_prompt=prompt_payload,
            attachments=attachments,
            file_doc=file_obj,
            tools_list=active_agent.get("tools", [])
        )
        
        full_response = st.write_stream(response_gen)

    # Update History
    st.session_state.chat_history[selected_agent_name].append({"role": "assistant", "content": full_response})
