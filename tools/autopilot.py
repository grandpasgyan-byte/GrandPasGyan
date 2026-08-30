"""
GrandPa's Gyan - Autopilot Security & Maintenance Sentinel
"""

import os
import sys
import time
import sqlite3
import gc
import streamlit as st

# Path configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "memory", "student_data.db")

class SystemAutopilot:
    def __init__(self):
        self.status = "Active"

    def run_health_checks(self):
        """Executes full diagnostic suite."""
        results = {
            "db_health": self._verify_and_repair_db(),
            "memory_cleaned": self._garbage_collection(),
            "api_status": self._verify_api_key(),
            "fs_integrity": self._check_directory_structure()
        }
        return results

    def _verify_and_repair_db(self):
        """Checks SQLite schema health and automatically repairs missing tables."""
        try:
            if not os.path.exists(os.path.dirname(DB_PATH)):
                os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Diagnostic check on main tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]

            required_tables = ["profile", "subject_progress", "activity_log"]
            missing = [t for t in required_tables if t not in tables]

            if missing:
                conn.close()
                from memory.student_memory import init_db
                init_db()
                return f"Repaired missing tables: {missing}"

            conn.close()
            return "Database Healthy"
        except Exception as e:
            return f"DB Autopilot Warning: {str(e)}"

    def _garbage_collection(self):
        """Cleans up unused memory and temporary upload buffers."""
        try:
            # Force Python garbage collector
            collected = gc.collect()
            
            # Trim chat history per session if memory exceeds limit
            if "chat_history" in st.session_state:
                for key in st.session_state.chat_history:
                    if len(st.session_state.chat_history[key]) > 40:
                        # Keep only the last 20 exchanges to avoid memory bloat
                        st.session_state.chat_history[key] = st.session_state.chat_history[key][-20:]

            return f"GC Executed ({collected} objects freed)"
        except Exception as e:
            return f"GC Error: {str(e)}"

    def _verify_api_key(self):
        """Validates Gemini API key availability without exposing secrets."""
        key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
        if not key:
            return "API Key Missing"
        if len(key) < 10:
            return "API Key Invalid Format"
        return "API Key Verified"

    def _check_directory_structure(self):
        """Ensures required folder structure and __init__.py files exist."""
        required_dirs = ["memory", "tools"]
        for d in required_dirs:
            dir_path = os.path.join(BASE_DIR, d)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            init_file = os.path.join(dir_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write("# Auto-generated package initializer\n")
        return "File Structure Validated"

# Singleton instance for background background lifecycle execution
autopilot_engine = SystemAutopilot()

def run_autopilot_sentinel():
    """Entry point function to call at app launch."""
    return autopilot_engine.run_health_checks()
