"""
GrandPa's Gyan - AI Educational Workspace
Main Streamlit Application File. Handles API integration, UI rendering, file parsing, and dynamic tool orchestration.
"""

import io
import time
from typing import List, Optional
import PyPDF2
from PIL import Image
from google import genai
from google.genai import types
from google.genai.errors import APIError
import streamlit as st

# Load Agent Database
from agents_registry import AGENTS_DATABASE

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GrandPa's Gyan - AI Student Workspace",
    page_icon="🧓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for Clean Dashboard UI
st.markdown(
    """
    <style:
    .stApp { background-color: #F8F9FA; }
    .stChatMessage { border-radius: 12px; padding: 12px; margin-bottom: 8px; }
    .stButton>button { border-radius: 8px; font-weight: 500; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SECURE API KEY SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None
if not api_key:
    api_key = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")

if not api_key:
    st.info("⚠️ Please enter a valid Gemini API Key (or configure Streamlit Secrets) to launch GrandPa's Gyan.")
    st.stop()

# Initialize GenAI Client
@st.cache_resource(show_spinner=False)
def init_genai_client(key: str) -> genai.Client:
    return genai.Client(api_key=key)

client = init_genai_client(api_key)

# --- SESSION STATE INITIALIZATION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "active_agent_name" not in st.session_state:
    st.session_state.active_agent_name = list(AGENTS_DATABASE.keys())[0]

# --- UTILITY & HELPER FUNCTIONS ---
def extract_text_from_pdf(pdf_file) -> str:
    """Extracts text contents safely from an uploaded PDF file."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text += f"\n--- Page {i+1} ---\n{text}"
        return extracted_text.strip()
    except Exception as e:
        st.error(f"Error reading PDF file: {str(e)}")
        return ""

def generate_audio_output(text: str) -> Optional[bytes]:
    """Generates audio bytes via gTTS for voice output."""
    try:
        from gtts import gTTS
        # Truncate text to limit processing time for audio preview
        clean_text = text[:400].replace("*", "").replace("#", "").replace("$", "")
        if not clean_text.strip():
            return None
        tts = gTTS(text=clean_text, lang="en", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None

def call_gemini_orchestrator(
    system_instruction: str,
    user_prompt: str,
    attached_image: Optional[Image.Image] = None,
    document_context: Optional[str] = None,
    use_search: bool = False,
    max_retries: int = 3,
) -> Optional[str]:
    """
    Central API execution pipeline. Handles multi-modal inputs,
    Google Search grounding, and rate-limit retries.
    """
    delay = 2
    
    # Construct Multimodal Contents Payload
    contents_payload = []
    
    if document_context:
        contents_payload.append(f"DOCUMENT CONTEXT:\n{document_context}\n\nUSER QUESTION:\n")
        
    contents_payload.append(user_prompt)
    
    if attached_image:
        contents_payload.append(attached_image)

    # Configure Google Search Grounding if required by tool
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.4,
    )
    
    if use_search:
        config.tools = [{"google_search": {}}]

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents_payload,
                config=config,
            )
            
            # Format Output Response + Grounding Sources if Search Was Used
            final_text = response.text or ""
            
            # Append Citations if returned by Search Grounding
            if use_search and hasattr(response, "candidates") and response.candidates:
                grounding_metadata = getattr(response.candidates[0], "grounding_metadata", None)
                if grounding_metadata and getattr(grounding_metadata, "grounding_chunks", None):
                    sources_text = "\n\n### 🔍 Sources Used:\n"
                    for chunk in grounding_metadata.grounding_chunks:
                        web_info = getattr(chunk, "web", None)
                        if web_info:
                            title = getattr(web_info, "title", "Source")
                            url = getattr(web_info, "uri", "#")
                            sources_text += f"* [{title}]({url})\n"
                    final_text += sources_text
                    
            return final_text

        except APIError as e:
            if getattr(e, "code", None) == 429:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    st.error("⏳ High server load detected. Please wait a few seconds before asking again.")
                    return None
            else:
                st.error(f"API Communication Error: {getattr(e, 'message', str(e))}")
                return None
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
            return None

# --- SIDEBAR & AGENT ROUTER ---
st.sidebar.title("🧓 GrandPa's Gyan")
st.sidebar.caption("Modular AI Student Workspace")

# Category Filter & Search
search_term = st.sidebar.text_input("🔍 Search Tools & Agents", "")
available_categories = ["All"] + sorted(list(set(a["category"] for a in AGENTS_DATABASE.values())))
selected_category = st.sidebar.selectbox("📂 Filter Category", available_categories)

# Filter Agents Dynamically
filtered_agents = {
    name: details for name, details in AGENTS_DATABASE.items()
    if (selected_category == "All" or details["category"] == selected_category)
    and (search_term.lower() in name.lower() or search_term.lower() in details["description"].lower())
}

st.sidebar.markdown("---")

if filtered_agents:
    agent_names = list(filtered_agents.keys())
    # Ensure selected agent stays valid
    if st.session_state.active_agent_name not in agent_names:
        st.session_state.active_agent_name = agent_names[0]
        
    st.session_state.active_agent_name = st.sidebar.radio(
        "Choose Active Agent:",
        options=agent_names,
        format_func=lambda x: f"{filtered_agents[x]['icon']} {x}",
    )

enable_voice = st.sidebar.toggle("🔊 Text-to-Speech Output", value=False)

# Clear History Button
if st.sidebar.button("🗑️ Clear Current Workspace"):
    st.session_state.chat_history[st.session_state.active_agent_name] = []
    st.rerun()

# --- MAIN WORKSPACE RENDERER ---
current_agent_name = st.session_state.active_agent_name
agent_config = AGENTS_DATABASE[current_agent_name]

# Active Agent Header
st.title(f"{agent_config['icon']} {current_agent_name}")
st.caption(agent_config["description"])

# Input Capability Badges
badge_str = " ".join([f"`{inp.upper()}`" for inp in agent_config["supported_inputs"]])
st.markdown(f"**Supported Inputs:** {badge_str}")

st.markdown("---")

# --- FILE & MULTI-MODAL ATTACHMENT CONTROLS ---
doc_text_context = None
attached_image_obj = None

# Show File Uploaders based on Agent Capabilities
col_file1, col_file2 = st.columns(2)

if "pdf" in agent_config["supported_inputs"]:
    with col_file1:
        uploaded_pdf = st.file_uploader("📄 Upload Study PDF / Document", type=["pdf"])
        if uploaded_pdf:
            with st.spinner("Extracting PDF content..."):
                doc_text_context = extract_text_from_pdf(uploaded_pdf)
                if doc_text_context:
                    st.success(f"Loaded PDF Context ({len(doc_text_context)} chars)")

if "image" in agent_config["supported_inputs"]:
    with col_file2:
        uploaded_img = st.file_uploader("🖼️ Upload Homework / Diagram Image", type=["png", "jpg", "jpeg"])
        if uploaded_img:
            attached_image_obj = Image.open(uploaded_img)
            st.image(attached_image_obj, caption="Uploaded Image Attachment", use_container_width=True)

# Initialize Session Chat History for Active Agent
if current_agent_name not in st.session_state.chat_history:
    st.session_state.chat_history[current_agent_name] = []

# Display Chat History
for msg in st.session_state.chat_history[current_agent_name]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "audio" in msg and msg["audio"]:
            st.audio(msg["audio"], format="audio/mp3")

# --- USER CHAT INPUT & EXECUTION ---
user_prompt = st.chat_input(f"Ask {current_agent_name}...")

if user_prompt:
    # 1. Render User Message
    st.session_state.chat_history[current_agent_name].append({"role": "user", "content": user_prompt})
    st.chat_message("user").markdown(user_prompt)

    # 2. Process via Gemini Orchestrator
    with st.chat_message("assistant"):
        with st.spinner(f"GrandPa is working on your request..."):
            
            use_search_grounding = "google_search" in agent_config["tools"]
            
            ai_response = call_gemini_orchestrator(
                system_instruction=agent_config["instruction"],
                user_prompt=user_prompt,
                attached_image=attached_image_obj,
                document_context=doc_text_context,
                use_search=use_search_grounding,
            )

            if ai_response:
                st.markdown(ai_response)
                
                # Generate Audio if Enabled
                audio_bytes = generate_audio_output(ai_response) if enable_voice else None
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")

                # Store Response in Chat History
                st.session_state.chat_history[current_agent_name].append({
                    "role": "assistant",
                    "content": ai_response,
                    "audio": audio_bytes,
                })
