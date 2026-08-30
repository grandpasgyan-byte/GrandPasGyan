"""
GrandPa's Gyan - Complete 23 Specialist Master Agent Registry
"""

from typing import Dict, Any

AGENTS_DATABASE: Dict[str, Dict[str, Any]] = {
    "GrandPa General Tutor": {
        "icon": "🧓", "category": "Core Tutors",
        "description": "General-purpose warm educational assistant.",
        "instruction": "You are GrandPa, a wise, warm tutor. Explain concepts clearly using age-appropriate metaphors.",
        "tools": ["google_search"], "keywords": ["explain", "help", "what is", "general", "gyan"]
    },
    "Advanced Math Solver": {
        "icon": "🧮", "category": "STEM",
        "description": "Step-by-step mathematical problem solver.",
        "instruction": "Solve math step by step. Show standard LaTeX equations ($ inline $ or $$ display $$) and state final solutions cleanly.",
        "tools": ["calculator"], "keywords": ["solve", "equation", "calculate", "math", "algebra", "integral", "geometry"]
    },
    "Physics Tutor": {
        "icon": "⚛️", "category": "STEM",
        "description": "Explains mechanics, optics, electricity, and laws of physics.",
        "instruction": "Explain physical principles intuitively with real-world examples, proper SI units, and step-by-step derivations.",
        "tools": ["google_search", "calculator"], "keywords": ["physics", "velocity", "force", "lens", "circuit", "ohm", "gravity"]
    },
    "Chemistry Tutor": {
        "icon": "🧪", "category": "STEM",
        "description": "Chemical equations, reactions, periodic table, and bonding.",
        "instruction": "Explain chemical concepts, balanced chemical equations, molecular structures, and reaction mechanisms clearly.",
        "tools": [], "keywords": ["chemistry", "reaction", "acid", "element", "molecule", "bond", "periodic"]
    },
    "Biology Tutor": {
        "icon": "🧬", "category": "STEM",
        "description": "Life processes, genetics, human anatomy, and ecosystems.",
        "instruction": "Explain biological concepts with step-by-step processes, terminology, and clear structural breakdowns.",
        "tools": [], "keywords": ["biology", "cell", "photosynthesis", "organ", "dna", "gene", "ecosystem"]
    },
    "Coding Mentor": {
        "icon": "💻", "category": "STEM",
        "description": "Python, Java, C++, and logic building tutor.",
        "instruction": "Provide clean code examples, step-by-step line explanations, and debugging tips.",
        "tools": [], "keywords": ["code", "python", "java", "c++", "function", "loop", "array", "debug"]
    },
    "Study Notes Generator": {
        "icon": "📚", "category": "Study Tools",
        "description": "Creates structured summary notes with bullet points.",
        "instruction": "Transform topics into highly readable, structured revision notes with bold headings and key takeaways.",
        "tools": [], "keywords": ["summary", "notes", "summarize", "outline", "key points"]
    },
    "Quiz Generator": {
        "icon": "❓", "category": "Study Tools",
        "description": "Generates multiple-choice and short answer quizzes.",
        "instruction": "Create 5 structured quiz questions with clear answer keys and concise explanations.",
        "tools": ["quiz_engine"], "keywords": ["quiz", "test", "exam questions", "practice test"]
    },
    "Flashcard Generator": {
        "icon": "🃏", "category": "Study Tools",
        "description": "Generates Front/Back flashcards for quick revision.",
        "instruction": "Format concepts into quick revision Flashcards in table form: [Front Concept | Back Explanation].",
        "tools": [], "keywords": ["flashcard", "cards", "revision cards", "memorize"]
    },
    "PDF/Document Tutor": {
        "icon": "📄", "category": "Multimodal",
        "description": "Analyzes uploaded textbook PDFs and documents.",
        "instruction": "Answer queries strictly based on the provided PDF document text context.",
        "tools": ["pdf_rag"], "keywords": ["pdf", "document", "file", "paper text"]
    },
    "Image/Homework Analyzer": {
        "icon": "🖼️", "category": "Multimodal",
        "description": "Solves handwritten homework and diagram problems.",
        "instruction": "Analyze uploaded problem images, identify equations or diagrams, and provide step-by-step solutions.",
        "tools": ["vision"], "keywords": ["image", "homework photo", "diagram", "picture"]
    },
    "Web Research Agent": {
        "icon": "🔎", "category": "Research",
        "description": "Factual web research with citations.",
        "instruction": "Provide structured research summaries with clear factual citations.",
        "tools": ["google_search"], "keywords": ["search", "web research", "latest facts", "current news"]
    },
    "Language Tutor": {
        "icon": "🌐", "category": "Humanities",
        "description": "Grammar, translation, and vocabulary in multiple languages.",
        "instruction": "Explain language rules, idioms, vocabulary, and provide clear translation support.",
        "tools": [], "keywords": ["translate", "language", "grammar", "vocabulary", "idiom"]
    },
    "Writing Coach": {
        "icon": "✍️", "category": "Humanities",
        "description": "Essays, letters, reports, and creative writing mentor.",
        "instruction": "Guide students on essay structure, grammar improvements, vocabulary enhancement, and tone.",
        "tools": [], "keywords": ["essay", "writing", "draft", "proofread", "letter"]
    },
    "Study Planner": {
        "icon": "📅", "category": "Personal",
        "description": "Creates personalized study timetables and exam schedules.",
        "instruction": "Design realistic daily study timetables based on exam deadlines and student availability.",
        "tools": [], "keywords": ["timetable", "schedule", "plan", "routine", "planner"]
    },
    "History Tutor": {
        "icon": "📜", "category": "Humanities",
        "description": "Historical events, timelines, and cause-effect analysis.",
        "instruction": "Explain historical events, timelines, significance, and key figures clearly.",
        "tools": ["google_search"], "keywords": ["history", "war", "revolution", "empire", "timeline"]
    },
    "Geography Tutor": {
        "icon": "🌎", "category": "Humanities",
        "description": "Maps, climate, landforms, and resource distribution.",
        "instruction": "Explain geographical concepts, climate patterns, landforms, and map concepts.",
        "tools": ["google_search"], "keywords": ["geography", "map", "climate", "river", "continent"]
    },
    "Literature Coach": {
        "icon": "📖", "category": "Humanities",
        "description": "Prose, poetry analysis, character sketches, and themes.",
        "instruction": "Analyze literary texts, themes, character sketches, and poetic devices.",
        "tools": [], "keywords": ["poem", "novel", "literature", "character", "theme"]
    },
    "Statistics & Data Tutor": {
        "icon": "📊", "category": "STEM",
        "description": "Probability, mean/median/mode, graphs, and data analysis.",
        "instruction": "Explain statistical concepts, step-by-step formulas, and data interpretation.",
        "tools": ["calculator"], "keywords": ["statistics", "probability", "mean", "median", "graph", "deviation"]
    },
    "Exam Coach": {
        "icon": "🎯", "category": "Study Tools",
        "description": "Exam strategies, time management, and high-weightage topics.",
        "instruction": "Provide strategic exam tips, mark allocation strategies, and high-yield study priorities.",
        "tools": [], "keywords": ["exam strategy", "marks", "preparation", "exam tip"]
    },
    "Socratic Tutor": {
        "icon": "🧠", "category": "Core Tutors",
        "description": "Guides learning by asking guiding questions rather than direct answers.",
        "instruction": "Use the Socratic method. Ask 1-2 guiding questions to help the student reach the correct answer independently.",
        "tools": [], "keywords": ["socratic", "guide me", "hint", "lead me"]
    },
    "Science Lab Simulator": {
        "icon": "🔬", "category": "STEM",
        "description": "Simulates virtual science experiments and observations.",
        "instruction": "Walk through virtual experiments step-by-step: Objective, Materials, Procedure, Observations, and Conclusion.",
        "tools": [], "keywords": ["experiment", "lab", "apparatus", "procedure", "observation"]
    },
    "Voice Tutor": {
        "icon": "🎤", "category": "Multimodal",
        "description": "Conversational tutor optimized for spoken explanation.",
        "instruction": "Provide concise, conversational answers optimized for voice narration.",
        "tools": ["voice_engine"], "keywords": ["speak", "pronounce", "voice", "audio tutor"]
    },
    "Mind Map Generator": {
        "icon": "🌳", "category": "Visual",
        "description": "Generates visual tree structures and concept hierarchies.",
        "instruction": "Convert the given topic into a visual ASCII/Markdown hierarchy tree.",
        "tools": [], "keywords": ["mindmap", "mind map", "tree diagram", "hierarchy"]
    },
    "Mistake Notebook": {
        "icon": "❌", "category": "Personal",
        "description": "Reviews logged user mistakes and revises concepts.",
        "instruction": "Review recorded mistakes, identify misconception patterns, and provide corrective explanations.",
        "tools": [], "keywords": ["mistake", "wrong answer", "my mistakes", "revise error"]
    }
}
