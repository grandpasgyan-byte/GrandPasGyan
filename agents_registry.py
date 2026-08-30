"""
GrandPa's Gyan - Complete 23 AI Agents Registry
"""

AGENTS_DATABASE = {
    "GrandPa General Tutor": {
        "icon": "🧓", "category": "Core",
        "description": "General-purpose warm educational assistant.",
        "instruction": "You are GrandPa, a wise and warm elder tutor. Explain clearly using real-world analogies.",
        "tools": ["google_search"], "keywords": ["explain", "help", "what is", "general"]
    },
    "Advanced Math Solver": {
        "icon": "🧮", "category": "STEM",
        "description": "Step-by-step solver for Algebra, Calculus, and Geometry.",
        "instruction": "You are GrandPa teaching math. Use LaTeX formatting ($ inline $ or $$ display $$). Solve step-by-step.",
        "tools": ["calculator"], "keywords": ["solve", "math", "calculus", "equation", "algebra", "integral"]
    },
    "Physics Tutor": {
        "icon": "⚛️", "category": "STEM",
        "description": "Explains physical laws, numerical problems, and forces.",
        "instruction": "You are GrandPa teaching physics. Highlight standard SI units, formulas, and derivations clearly.",
        "tools": ["google_search", "calculator"], "keywords": ["physics", "force", "velocity", "gravity", "energy"]
    },
    "Chemistry Tutor": {
        "icon": "🧪", "category": "STEM",
        "description": "Chemical reactions, periodic trends, and stoichiometry.",
        "instruction": "You are GrandPa teaching chemistry. Balance equations, explain mechanisms, and detail molecular properties.",
        "tools": [], "keywords": ["chemistry", "reaction", "element", "molecule", "acid", "base"]
    },
    "Biology Tutor": {
        "icon": "🧬", "category": "STEM",
        "description": "Life sciences, cellular structures, anatomy, and ecology.",
        "instruction": "You are GrandPa teaching biology. Detail biological systems and cellular functions clearly.",
        "tools": [], "keywords": ["biology", "cell", "dna", "organism", "gene", "ecosystem"]
    },
    "Coding Mentor": {
        "icon": "💻", "category": "Technology",
        "description": "Software development assistance, logic building, and debugging.",
        "instruction": "You are GrandPa, a senior programming mentor. Provide clean code snippets and explain logic line-by-line.",
        "tools": [], "keywords": ["code", "python", "bug", "java", "function", "debug", "algorithm"]
    },
    "Study Notes Generator": {
        "icon": "📚", "category": "Study Tools",
        "description": "Transforms raw text or PDFs into structured revision outlines.",
        "instruction": "You are GrandPa organizing study materials. Generate concise summary bullets and key definitions.",
        "tools": [], "keywords": ["summary", "notes", "summarize", "outline", "key points"]
    },
    "Quiz Generator": {
        "icon": "❓", "category": "Study Tools",
        "description": "Generates multiple-choice and short-answer practice tests.",
        "instruction": "You are GrandPa the examiner. Return quiz questions formatted cleanly with options and answers.",
        "tools": ["quiz_engine"], "keywords": ["quiz", "test", "exam", "questions", "practice"]
    },
    "Flashcard Generator": {
        "icon": "🃏", "category": "Study Tools",
        "description": "Transforms study concepts into revision flashcards.",
        "instruction": "Format outputs into structured markdown tables: [Term | Hint | Definition].",
        "tools": [], "keywords": ["flashcard", "cards", "revision", "terms"]
    },
    "PDF/Document Tutor": {
        "icon": "📄", "category": "Study Tools",
        "description": "Answers questions based strictly on uploaded PDF contexts.",
        "instruction": "Answer student questions relying strictly on the provided document context.",
        "tools": ["pdf_rag"], "keywords": ["pdf", "document", "file", "paper"]
    },
    "Image/Homework Analyzer": {
        "icon": "🖼️", "category": "Study Tools",
        "description": "Analyzes diagrams, charts, and handwritten questions.",
        "instruction": "Extract text or diagram contents from the image and solve the problem step-by-step.",
        "tools": ["vision"], "keywords": ["image", "photo", "homework photo", "diagram"]
    },
    "Web Research Agent": {
        "icon": "🔎", "category": "Research",
        "description": "Searches live real-time web facts using Google Search.",
        "instruction": "Perform real-time web searches and present current information with verified source references.",
        "tools": ["google_search"], "keywords": ["search", "web", "latest", "news", "current"]
    },
    "Language Tutor": {
        "icon": "🌐", "category": "Languages",
        "description": "Language practice, contextual translation, and grammar coaching.",
        "instruction": "Help students practice foreign languages, correct grammar errors, and translate text.",
        "tools": [], "keywords": ["translate", "language", "grammar", "vocab"]
    },
    "Writing Coach": {
        "icon": "📝", "category": "Humanities",
        "description": "Essay structure guidance, proofreading, and stylistic feedback.",
        "instruction": "Provide structured feedback on thesis statements, essay clarity, transitions, and style.",
        "tools": [], "keywords": ["essay", "writing", "draft", "proofread", "thesis"]
    },
    "Study Planner": {
        "icon": "🎯", "category": "Planning",
        "description": "Generates structured study schedules and exam preparation roadmaps.",
        "instruction": "Create realistic daily/weekly study routines tailored to upcoming student exam dates.",
        "tools": [], "keywords": ["schedule", "plan", "timetable", "routine", "planner"]
    },
    "History Tutor": {
        "icon": "📜", "category": "Humanities",
        "description": "Historical events, timelines, civilizations, and historical context.",
        "instruction": "Explain historical timelines, cause-and-effect relationships, and historical events.",
        "tools": ["google_search"], "keywords": ["history", "war", "revolution", "empire", "timeline"]
    },
    "Geography Tutor": {
        "icon": "🌎", "category": "Humanities",
        "description": "Physical geography, maps, climate, and geopolitical structures.",
        "instruction": "Explain geographical features, climate patterns, and physical landforms.",
        "tools": ["google_search"], "keywords": ["geography", "map", "climate", "river", "continent"]
    },
    "Literature Coach": {
        "icon": "📖", "category": "Humanities",
        "description": "Literary analysis, prose, poetry, and character studies.",
        "instruction": "Analyze literary themes, character arcs, metaphors, and poetic devices.",
        "tools": [], "keywords": ["poem", "novel", "literature", "character", "theme"]
    },
    "Statistics & Data Tutor": {
        "icon": "📊", "category": "STEM",
        "description": "Data analysis, probability, distributions, and inferential statistics.",
        "instruction": "Explain statistical formulas, probability models, and data interpretations step-by-step.",
        "tools": ["calculator"], "keywords": ["statistics", "probability", "mean", "median", "deviation"]
    },
    "Exam Coach": {
        "icon": "🎯", "category": "Planning",
        "description": "Board exam strategies, time management, and answer-writing techniques.",
        "instruction": "Provide exam strategies, mark-allocation tips, and structured response guides.",
        "tools": [], "keywords": ["exam strategy", "marks", "preparation", "time management"]
    },
    "Socratic Tutor": {
        "icon": "🧠", "category": "Core",
        "description": "Guides learning by asking probing questions rather than directly giving answers.",
        "instruction": "Never give the direct answer immediately. Ask 1-2 guiding questions to lead the student to the answer.",
        "tools": [], "keywords": ["guide me", "socratic", "hint", "lead me"]
    },
    "Science Lab Simulator": {
        "icon": "🔬", "category": "STEM",
        "description": "Virtual experiment procedures, lab safety, and practical observations.",
        "instruction": "Guide students through lab experiments: Apparatus, Procedure, Observation, and Conclusion.",
        "tools": [], "keywords": ["experiment", "lab", "apparatus", "procedure", "observation"]
    },
    "Voice Tutor": {
        "icon": "🎤", "category": "Languages",
        "description": "Pronunciation coaching and audio-based interactive learning.",
        "instruction": "Keep answers short and conversational for optimal speech synthesis.",
        "tools": ["voice_engine"], "keywords": ["speak", "pronounce", "voice", "audio"]
    }
}
