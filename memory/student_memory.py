"""
GrandPa's Gyan - Persistent Student Memory & Performance Database
"""

import sqlite3
import datetime
from typing import Dict, Any, List

DB_PATH = "grandpa_memory.db"

def init_db():
    """Initializes SQLite database tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Student profile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profile (
            id INTEGER PRIMARY KEY DEFAULT 1,
            name TEXT DEFAULT 'Student',
            board TEXT DEFAULT 'CBSE / NCERT',
            grade TEXT DEFAULT 'Class 10',
            preferred_language TEXT DEFAULT 'English',
            font_size TEXT DEFAULT 'Medium'
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO student_profile (id) VALUES (1)")
    
    # Subject progress
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject_progress (
            subject TEXT PRIMARY KEY,
            score_sum INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            level TEXT DEFAULT 'Medium'
        )
    """)
    
    # Activity log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_used TEXT,
            timestamp TEXT
        )
    """)
    
    default_subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Coding", "General"]
    for subj in default_subjects:
        cursor.execute("INSERT OR IGNORE INTO subject_progress (subject, score_sum, attempts, level) VALUES (?, 0, 0, 'Medium')", (subj,))
        
    conn.commit()
    conn.close()

def get_profile() -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, board, grade, preferred_language, font_size FROM student_profile WHERE id=1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "board": row[1], "grade": row[2], "language": row[3], "font_size": row[4]}
    return {"name": "Student", "board": "CBSE / NCERT", "grade": "Class 10", "language": "English", "font_size": "Medium"}

def update_profile(name: str, board: str, grade: str, language: str, font_size: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE student_profile 
        SET name=?, board=?, grade=?, preferred_language=?, font_size=? 
        WHERE id=1
    """, (name, board, grade, language, font_size))
    conn.commit()
    conn.close()

def log_activity(agent_name: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO activity_log (agent_used, timestamp) VALUES (?, ?)", (agent_name, now_str))
    conn.commit()
    conn.close()

def record_quiz_score(subject: str, score_percent: int):
    """Adaptive learning rule: Adjusts difficulty based on target score."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT score_sum, attempts FROM subject_progress WHERE subject=?", (subject,))
    row = cursor.fetchone()
    if row:
        new_sum = row[0] + score_percent
        new_attempts = row[1] + 1
        avg = new_sum / new_attempts
        
        new_level = "Hard" if avg > 80 else ("Easy" if avg < 45 else "Medium")
        cursor.execute("""
            UPDATE subject_progress 
            SET score_sum=?, attempts=?, level=? 
            WHERE subject=?
        """, (new_sum, new_attempts, new_level, subject))
    conn.commit()
    conn.close()

def get_student_stats() -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT subject, score_sum, attempts, level FROM subject_progress")
    rows = cursor.fetchall()
    
    scores = {}
    levels = {}
    weakest_subject = "Mathematics"
    lowest_avg = 101.0
    
    for subj, score_sum, attempts, level in rows:
        avg = round((score_sum / attempts), 1) if attempts > 0 else 50.0
        scores[subj] = avg
        levels[subj] = level
        if avg < lowest_avg:
            lowest_avg = avg
            weakest_subject = subj
            
    cursor.execute("SELECT COUNT(DISTINCT DATE(timestamp)) FROM activity_log")
    streak_days = cursor.fetchone()[0] or 1
    
    cursor.execute("SELECT COUNT(*) FROM activity_log")
    total_interactions = cursor.fetchone()[0] or 0
    conn.close()
    
    return {
        "scores": scores,
        "levels": levels,
        "weakest_subject": weakest_subject,
        "streak_days": streak_days,
        "total_interactions": total_interactions
    }
