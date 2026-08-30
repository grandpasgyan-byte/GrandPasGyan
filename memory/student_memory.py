"""
Student Memory Engine - Persistent Local SQLite Storage
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_data.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create profile table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT DEFAULT 'Student',
            board TEXT DEFAULT 'CBSE',
            grade TEXT DEFAULT 'Class 10',
            language TEXT DEFAULT 'English',
            font_size TEXT DEFAULT 'Standard'
        )
    """)

    # Seed initial default profile if not present
    cursor.execute("""
        INSERT OR IGNORE INTO profile (id, name, board, grade, language, font_size)
        VALUES (1, 'Student', 'CBSE', 'Class 10', 'English', 'Standard')
    """)

    # Create subject progress table WITH UNIQUE CONSTRAINT on subject
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject_progress (
            subject TEXT PRIMARY KEY,
            score_sum REAL DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            level TEXT DEFAULT 'Medium'
        )
    """)

    # Seed default subject rows safely
    default_subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "General"]
    for subj in default_subjects:
        cursor.execute("""
            INSERT OR IGNORE INTO subject_progress (subject, score_sum, attempts, level)
            VALUES (?, 0, 0, 'Medium')
        """, (subj,))

    # Create activity history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def get_profile():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, board, grade, language, font_size FROM profile WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "board": row[1], "grade": row[2], "language": row[3], "font_size": row[4]}
    return {"name": "Student", "board": "CBSE", "grade": "Class 10", "language": "English", "font_size": "Standard"}

def update_profile(name, board, grade, language, font_size):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE profile
        SET name = ?, board = ?, grade = ?, language = ?, font_size = ?
        WHERE id = 1
    """, (name, board, grade, language, font_size))
    conn.commit()
    conn.close()

def log_activity(agent_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO activity_log (agent_name) VALUES (?)", (agent_name,))
    conn.commit()
    conn.close()

def record_quiz_score(subject, score):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ensure subject entry exists
    cursor.execute("INSERT OR IGNORE INTO subject_progress (subject, score_sum, attempts, level) VALUES (?, 0, 0, 'Medium')", (subject,))
    
    cursor.execute("""
        UPDATE subject_progress
        SET score_sum = score_sum + ?, attempts = attempts + 1
        WHERE subject = ?
    """, (score, subject))
    
    # Recalculate level
    cursor.execute("SELECT score_sum, attempts FROM subject_progress WHERE subject = ?", (subject,))
    row = cursor.fetchone()
    if row and row[1] > 0:
        avg = row[0] / row[1]
        new_lvl = "Easy" if avg < 40 else ("Hard" if avg > 75 else "Medium")
        cursor.execute("UPDATE subject_progress SET level = ? WHERE subject = ?", (new_lvl, subject))
        
    conn.commit()
    conn.close()

def get_student_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM activity_log")
    total_interactions = cursor.fetchone()[0]
    
    cursor.execute("SELECT subject, score_sum, attempts, level FROM subject_progress")
    rows = cursor.fetchall()
    
    scores = {}
    levels = {}
    weakest_subj = "None"
    min_avg = 101
    
    for row in rows:
        subj, score_sum, attempts, level = row
        avg = (score_sum / attempts) if attempts > 0 else 0
        scores[subj] = round(avg, 1)
        levels[subj] = level
        
        if attempts > 0 and avg < min_avg:
            min_avg = avg
            weakest_subj = subj
            
    conn.close()
    
    return {
        "streak_days": 3,
        "total_interactions": total_interactions,
        "weakest_subject": weakest_subj if weakest_subj != "None" else "Physics",
        "scores": scores,
        "levels": levels
    }
