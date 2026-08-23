import io
import time
from agents_registry import AGENTS_DATABASE
from google import genai
from google.genai import types
from google.genai.errors import APIError
from gtts import gTTS
import streamlit as st

st.set_page_config(page_title="GrandPa's Gyan", page_icon="👴", layout="wide")

# Secure API Key Loading
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("⚠️ Please configure your free Gemini API Key to open GrandPa's Gyan.")
    st.stop()

client = genai.Client(api_key=api_key)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "active_agent" not in st.session_state:
    st.session_state.active_agent = list(AGENTS_DATABASE.keys())[0]

def call_gemini_safe(system_instruction, user_prompt, max_retries=3):
    delay = 2
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(system_instruction=system_instruction)
            )
            return response.text
        except APIError as e:
            if e.code == 429:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    st.error("⏳ High global traffic. Please wait a moment.")
                    return None
            else:
                st.error(f"API Error: {e.message}")
                return None

def get_audio(text):
    try:
        tts = gTTS(text=text[:300], lang="en")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None

# Sidebar Setup
st.sidebar.title("👴 GrandPa's Gyan")
st.sidebar.caption("Wise, Patient & Free AI Learning")

search_query = st.sidebar.text_input("🔍 Search GrandPa's Wisdom Tools", "")
categories = ["All"] + sorted(list(set(a["category"] for a in AGENTS_DATABASE.values())))
selected_cat = st.sidebar.selectbox("📂 Category Filter", categories)

filtered_agents = {
    name: details for name, details in AGENTS_DATABASE.items()
    if (selected_cat == "All" or details["category"] == selected_cat)
    and (search_query.lower() in name.lower() or search_query.lower() in details["instruction"].lower())
}

st.sidebar.markdown("---")
if filtered_agents:
    st.session_state.active_agent = st.sidebar.radio(
        "Choose Wisdom Mode:",
        options=list(filtered_agents.keys()),
        format_func=lambda x: f"{filtered_agents[x]['icon']} {x}"
    )

enable_audio = st.sidebar.toggle("🔊 Audio Voice Output", value=True)

# Workspace Interface
active_name = st.session_state.active_agent
active_info = AGENTS_DATABASE[active_name]

st.title(f"{active_info['icon']} {active_name}")
st.markdown("*Welcome to your cozy corner of wisdom! Ask GrandPa anything.*")

if active_name not in st.session_state.chat_history:
    st.session_state.chat_history[active_name] = []

for msg in st.session_state.chat_history[active_name]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "audio" in msg and msg["audio"]:
            st.audio(msg["audio"], format="audio/mp3")

if user_input := st.chat_input(f"Ask {active_name}..."):
    st.session_state.chat_history[active_name].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("GrandPa is thinking..."):
        full_instruction = f"{active_info['instruction']}\nMaintain a warm, patient, grandparent-like tone."
        reply = call_gemini_safe(system_instruction=full_instruction, user_prompt=user_input)

        if reply:
            audio_bytes = get_audio(reply) if enable_audio else None
            st.session_state.chat_history[active_name].append({
                "role": "assistant",
                "content": reply,
                "audio": audio_bytes
            })
            with st.chat_message("assistant"):
                st.write(reply)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")