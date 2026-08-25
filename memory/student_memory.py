"""
GrandPa's Gyan - Student Memory & Persistence Layer
Uses SQLite for zero-dependency persistent storage of user progress and stats.
"""

import sqlite3
import datetime
from typing import Dict, Any

DB_PATH = "grandpa_memory.db"

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Progress tracking per subject
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject_progress (
            subject TEXT PRIMARY KEY,
            score_sum INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0
        )
    """)
    
    # User study activity log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_used TEXT,
            timestamp TEXT
        )
    """)
    
    # Default STEM categories initialization
    default_subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Coding"]
    for subj in default_subjects:
        cursor.execute("INSERT OR IGNORE INTO subject_progress (subject, score_sum, attempts) VALUES (?, 0, 0)", (subj,))
        
    conn.commit()
    conn.close()

def log_activity(agent_name: str):
    """Logs an interaction with a specific agent."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO activity_log (agent_used, timestamp) VALUES (?, ?)", (agent_name, now_str))
    conn.commit()
    conn.close()

def record_quiz_score(subject: str, score_percent: int):
    """Updates subject mastery percentage after a quiz or practice session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE subject_progress 
        SET score_sum = score_sum + ?, attempts = attempts + 1 
        WHERE subject = ?
    """, (score_percent, subject))
    conn.commit()
    conn.close()

def get_student_stats() -> Dict[str, Any]:
    """Retrieves student progress analytics for dashboard rendering."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Calculate subject averages
    cursor.execute("SELECT subject, score_sum, attempts FROM subject_progress")
    rows = cursor.fetchall()
    scores = {}
    weakest_subject = "Mathematics"
    lowest_avg = 101.0
    
    for subj, score_sum, attempts in rows:
        avg = round((score_sum / attempts), 1) if attempts > 0 else 50.0
        scores[subj] = avg
        if avg < lowest_avg:
            lowest_avg = avg
            weakest_subject = subj
            
    # Calculate activity counts
    cursor.execute("SELECT COUNT(DISTINCT DATE(timestamp)) FROM activity_log")
    streak_days = cursor.fetchone()[0] or 1
    
    cursor.execute("SELECT COUNT(*) FROM activity_log")
    total_interactions = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "scores": scores,
        "weakest_subject": weakest_subject,
        "streak_days": streak_days,
        "total_interactions": total_interactions
    }
