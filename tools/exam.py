"""
Exam Intelligence & Previous Year Paper Analyzer
"""

from typing import Dict, Any

def generate_exam_analysis_prompt(paper_text: str, subject: str) -> str:
    return f"""
You are an expert Examination Board Analyst for {subject}.
Analyze the provided previous year question paper text and extract:
1. High-Frequency / Repeated Topics
2. Chapter-wise Marks Distribution
3. Difficulty Trend (Easy / Medium / Hard)
4. Top 5 Must-Revise Topics

Question Paper Text:
{paper_text}
"""
