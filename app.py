"""
GrandPa's Gyan - Main Streamlit Application
"""

import streamlit as st

# Local Modules
from config import get_api_key
from agents_registry import AGENTS_DATABASE
from agent_router import route_agent
from gemini_service import stream_gemini_response
from tools.pdf import extract_pdf_text
from tools.vision import process_image
from tools.web_search import is_search_enabled

# Page Setup
st.set_page_config(
    page_title="GrandPa's Gyan",
    page_icon="🧓",
    layout="wide"
)

# API Key Validation
api_key = get_api_key()
if not api_key:
    api_key_input = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")
    if not api_key_input:
        st.info("⚠️ Please enter your Gemini API Key in the sidebar or setup Streamlit Secrets to run GrandPa's Gyan.")
        st.stop()
    st.secrets["GEMINI_API_KEY"] = api_key_input

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# Sidebar Agent Selection
st.sidebar.title("🧓 GrandPa's Gyan")
st.sidebar.caption("Modular AI Educational Workspace")

category_filter = st.sidebar.selectbox(
    "📂 Category Filter", 
    ["All"] + sorted(list(set(a["category"] for a in AGENTS_DATABASE.values())))
)

filtered_agent_names = [
    name for name, details in AGENTS_DATABASE.items()
    if category_filter == "All" or details["category"] == category_filter
]

selected_agent_name = st.sidebar.radio(
    "Choose Active Agent:",
    filtered_agent_names,
    format_func=lambda x: f"{AGENTS_DATABASE[x]['icon']} {x}"
)

# Fetch Current Agent Details
active_agent = route_agent(selected_agent_name)

# Active Agent Header
st.title(f"{active_agent['icon']} {selected_agent_name}")
st.caption(active_agent["description"])

# Initialize History for current agent
if selected_agent_name not in st.session_state.chat_history:
    st.session_state.chat_history[selected_agent_name] = []

# Display Existing Chat History
for msg in st.session_state.chat_history[selected_agent_name]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Multi-Modal Upload Controls via Expandable Container
with st.expander("📎 Attach Documents or Images (Optional)"):
    col1, col2 = st.columns(2)
    with col1:
        uploaded_pdf = st.file_uploader("Upload PDF Document", type=["pdf"], key=f"pdf_{selected_agent_name}")
    with col2:
        uploaded_image = st.file_uploader("Upload Homework / Diagram Image", type=["png", "jpg", "jpeg"], key=f"img_{selected_agent_name}")

# User Input Box
user_input = st.chat_input(f"Ask {selected_agent_name}...")

if user_input:
    # Append User Input to History & Render
    st.session_state.chat_history[selected_agent_name].append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Process Attachments
    attachments = []
    pdf_text = None

    if uploaded_pdf:
        pdf_text = extract_pdf_text(uploaded_pdf)
        if pdf_text:
            st.info(f"📄 Attached PDF context ({len(pdf_text)} characters)")

    if uploaded_image:
        img_obj = process_image(uploaded_image)
        if img_obj:
            attachments.append(img_obj)
            st.image(img_obj, caption="Attached Image", width=250)

    # Formulate Prompt Payload with PDF context if available
    full_prompt = user_input
    if pdf_text:
        full_prompt = f"--- ATTACHED PDF CONTEXT ---\n{pdf_text}\n\n--- USER INQUIRY ---\n{user_input}"

    # Streaming Assistant Response
    with st.chat_message("assistant"):
        use_search = is_search_enabled(active_agent)
        
        response_generator = stream_gemini_response(
            system_instruction=active_agent["instruction"],
            user_prompt=full_prompt,
            attachments=attachments,
            use_search=use_search
        )
        
        full_response = st.write_stream(response_generator)

    # Store Response in History
    st.session_state.chat_history[selected_agent_name].append({"role": "assistant", "content": full_response})
