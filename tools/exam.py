"""
GrandPa's Gyan - Exam Intelligence & Previous Year Paper Analyzer
"""

def generate_exam_analysis_prompt(paper_text: str, subject: str) -> str:
    """Generates structured prompt for question paper trend extraction."""
    return f"""
You are an expert Examination Board Trend Analyst for {subject}.
Analyze the provided previous year question paper text and extract:
1. High-Frequency / Repeated Topics
2. Chapter-wise Marks Distribution
3. Difficulty Trend (Easy / Medium / Hard)
4. Top 5 Must-Revise High-Yield Topics

Question Paper Content:
{paper_text}
"""
