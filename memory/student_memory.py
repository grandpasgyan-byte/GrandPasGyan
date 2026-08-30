"""
GrandPa's Gyan - Student Memory & Persistence Storage Engine
Manages SQLite database for profiles, activity logs, mistakes, bookmarks, and adaptive metrics.
"""

import sqlite3
import datetime
from typing import Dict, Any, List

DB_PATH = "student_memory.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    """Initializes tables for profile, activity logs, mistakes, bookmarks, and performance."""
    conn = get_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY,
        name TEXT, board TEXT, grade TEXT, language TEXT, font_size TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS mistakes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT, question TEXT, user_answer TEXT, correct_answer TEXT, concept TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, content TEXT, category TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS subject_progress (
        subject TEXT PRIMARY KEY,
        score_sum INTEGER DEFAULT 0,
        attempts INTEGER DEFAULT 0,
        level TEXT DEFAULT 'Medium'
    )''')

    c.execute("SELECT COUNT(*) FROM profile")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO profile VALUES (1, 'Student', 'CBSE / NCERT', 'Class 10', 'English', 'Standard')")

    default_subjects = ["Mathematics", "Science", "Physics", "Chemistry", "Biology", "English", "General"]
    for subj in default_subjects:
        c.execute("INSERT OR IGNORE INTO subject_progress (subject, score_sum, attempts, level) VALUES (?, 0, 0, 'Medium')", (subj,))

    conn.commit()
    conn.close()

def get_profile() -> Dict[str, str]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name, board, grade, language, font_size FROM profile WHERE id=1")
    row = c.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "board": row[1], "grade": row[2], "language": row[3], "font_size": row[4]}
    return {"name": "Student", "board": "CBSE / NCERT", "grade": "Class 10", "language": "English", "font_size": "Standard"}

def update_profile(name: str, board: str, grade: str, language: str, font_size: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE profile SET name=?, board=?, grade=?, language=?, font_size=? WHERE id=1",
              (name, board, grade, language, font_size))
    conn.commit()
    conn.close()

def log_activity(agent_name: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO activity_log (agent_name) VALUES (?)", (agent_name,))
    conn.commit()
    conn.close()

def log_mistake(subject: str, question: str, user_ans: str, correct_ans: str, concept: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO mistakes (subject, question, user_answer, correct_answer, concept) VALUES (?,?,?,?,?)",
              (subject, question, user_ans, correct_ans, concept))
    conn.commit()
    conn.close()

def get_mistakes() -> List[Dict[str, str]]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT subject, question, user_answer, correct_answer, concept FROM mistakes")
    rows = c.fetchall()
    conn.close()
    return [{"subject": r[0], "question": r[1], "user_answer": r[2], "correct_answer": r[3], "concept": r[4]} for r in rows]

def save_bookmark(title: str, content: str, category: str = "General"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO bookmarks (title, content, category) VALUES (?,?,?)", (title, content, category))
    conn.commit()
    conn.close()

def get_bookmarks() -> List[Dict[str, str]]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT title, content, category FROM bookmarks")
    rows = c.fetchall()
    conn.close()
    return [{"title": r[0], "content": r[1], "category": r[2]} for r in rows]

def record_quiz_score(subject: str, score_percent: int):
    """Adaptive learning rule: Dynamically adjusts level based on score trends."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT score_sum, attempts FROM subject_progress WHERE subject=?", (subject,))
    row = c.fetchone()
    if row:
        new_sum = row[0] + score_percent
        new_attempts = row[1] + 1
        avg = new_sum / new_attempts
        new_level = "Hard" if avg > 80 else ("Easy" if avg < 45 else "Medium")
        c.execute("UPDATE subject_progress SET score_sum=?, attempts=?, level=? WHERE subject=?",
                  (new_sum, new_attempts, new_level, subject))
    conn.commit()
    conn.close()

def get_student_stats() -> Dict[str, Any]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT subject, score_sum, attempts, level FROM subject_progress")
    rows = c.fetchall()

    scores = {}
    levels = {}
    weakest_subject = "Mathematics"
    lowest_avg = 101.0

    for subj, score_sum, attempts, level in rows:
        avg = round((score_sum / attempts), 1) if attempts > 0 else 75.0
        scores[subj] = avg
        levels[subj] = level
        if avg < lowest_avg:
            lowest_avg = avg
            weakest_subject = subj

    c.execute("SELECT COUNT(DISTINCT DATE(timestamp)) FROM activity_log")
    streak_row = c.fetchone()
    streak_days = streak_row[0] if (streak_row and streak_row[0] > 0) else 1

    c.execute("SELECT COUNT(*) FROM activity_log")
    total_interactions = c.fetchone()[0]
    conn.close()

    return {
        "streak_days": streak_days,
        "total_interactions": total_interactions,
        "weakest_subject": weakest_subject,
        "scores": scores,
        "levels": levels
    }
