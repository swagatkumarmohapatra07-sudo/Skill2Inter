"""
Seed script — loads sample students and internships into the database.
Run automatically on first startup if the database is empty.
"""
import json
from sqlalchemy.orm import Session
from app.models.student import Student, StudentSkill, Project
from app.models.internship import Internship, InternshipRequirement

# ── Sample Students ───────────────────────────────────────────────────────────

SAMPLE_STUDENTS = [
    {
        "name": "Arjun Sharma",
        "email": "arjun.demo@skill2inter.com",
        "password_hash": "demo",
        "college": "IIT Bombay",
        "degree": "B.Tech",
        "branch": "Computer Science",
        "graduation_year": 2025,
        "cgpa": 8.4,
        "location": "Mumbai",
        "preferred_location": "Remote",
        "remote_preference": "remote",
        "availability": "3 months",
        "bio": "Passionate about AI/ML. 2 ML projects on GitHub.",
        "skills": [
            {"skill_name": "Python", "category": "programming", "proficiency": "advanced"},
            {"skill_name": "Machine Learning", "category": "ml", "proficiency": "intermediate"},
            {"skill_name": "SQL", "category": "database", "proficiency": "intermediate"},
            {"skill_name": "Pandas", "category": "ml", "proficiency": "intermediate"},
            {"skill_name": "NumPy", "category": "ml", "proficiency": "intermediate"},
            {"skill_name": "Scikit-learn", "category": "ml", "proficiency": "intermediate"},
            {"skill_name": "HTML", "category": "web", "proficiency": "beginner"},
            {"skill_name": "CSS", "category": "web", "proficiency": "beginner"},
        ],
        "projects": [
            {
                "title": "Weather Prediction System",
                "description": "ML model predicting rainfall using historical weather data",
                "technologies": "python,scikit-learn,pandas,matplotlib,flask",
            },
            {
                "title": "Student Performance Analyzer",
                "description": "Regression model to predict student grades from activity data",
                "technologies": "python,pandas,numpy,sklearn,jupyter",
            },
        ],
    },
    {
        "name": "Priya Nair",
        "email": "priya.demo@skill2inter.com",
        "password_hash": "demo",
        "college": "VIT Vellore",
        "degree": "B.Tech",
        "branch": "Information Technology",
        "graduation_year": 2025,
        "cgpa": 8.8,
        "location": "Chennai",
        "preferred_location": "Bangalore",
        "remote_preference": "open",
        "availability": "6 months",
        "bio": "Java backend developer with Spring Boot experience.",
        "skills": [
            {"skill_name": "Java", "category": "programming", "proficiency": "advanced"},
            {"skill_name": "Spring Boot", "category": "web", "proficiency": "intermediate"},
            {"skill_name": "SQL", "category": "database", "proficiency": "advanced"},
            {"skill_name": "MySQL", "category": "database", "proficiency": "intermediate"},
            {"skill_name": "Git", "category": "tool", "proficiency": "intermediate"},
            {"skill_name": "REST API", "category": "web", "proficiency": "intermediate"},
            {"skill_name": "Maven", "category": "tool", "proficiency": "beginner"},
        ],
        "projects": [
            {
                "title": "E-Commerce Backend",
                "description": "Full REST API for e-commerce with Spring Boot and MySQL",
                "technologies": "java,spring boot,mysql,rest api,maven",
            },
            {
                "title": "Library Management System",
                "description": "CRUD application with Spring Security and JWT auth",
                "technologies": "java,spring boot,mysql,jwt,git",
            },
        ],
    },
    {
        "name": "Riya Patel",
        "email": "riya.demo@skill2inter.com",
        "password_hash": "demo",
        "college": "NMIMS Mumbai",
        "degree": "B.Tech",
        "branch": "Computer Science",
        "graduation_year": 2026,
        "cgpa": 7.9,
        "location": "Mumbai",
        "preferred_location": "Remote",
        "remote_preference": "remote",
        "availability": "3 months",
        "bio": "Frontend developer focused on React and UI/UX.",
        "skills": [
            {"skill_name": "HTML", "category": "web", "proficiency": "advanced"},
            {"skill_name": "CSS", "category": "web", "proficiency": "advanced"},
            {"skill_name": "JavaScript", "category": "programming", "proficiency": "advanced"},
            {"skill_name": "React", "category": "web", "proficiency": "intermediate"},
            {"skill_name": "Figma", "category": "tool", "proficiency": "intermediate"},
            {"skill_name": "Git", "category": "tool", "proficiency": "intermediate"},
            {"skill_name": "Tailwind", "category": "web", "proficiency": "intermediate"},
        ],
        "projects": [
            {
                "title": "Portfolio Website",
                "description": "Responsive personal portfolio built with React",
                "technologies": "react,css,javascript,html,git",
            },
            {
                "title": "Weather Dashboard",
                "description": "React weather app consuming OpenWeather API",
                "technologies": "react,javascript,css,rest api,html",
            },
        ],
    },
]

# ── Sample Internships ────────────────────────────────────────────────────────

SAMPLE_INTERNSHIPS = [
    # ── AI / ML ──────────────────────────────────────────────────────────────
    {
        "company": "DataSense AI",
        "title": "Python AI/ML Intern",
        "domain": "AI/ML",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹15,000/month",
        "deadline": "2025-02-15",
        "experience_required": "Freshers",
        "education_required": "B.Tech CSE/IT/ECE",
        "description": "Join our AI team to build ML models for real-world datasets. Work with Python, Pandas, and scikit-learn. Freshers with ML projects welcome.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Machine Learning", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Pandas", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "NumPy", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "SQL", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "Docker", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "REST API", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 0.9},
            {"requirement": "Freshers", "category": "experience", "mandatory": False, "importance": 0.5},
        ],
    },
    {
        "company": "NeuralWave Labs",
        "title": "Deep Learning Research Intern",
        "domain": "AI/ML",
        "location": "Bangalore",
        "work_mode": "hybrid",
        "duration": "6 months",
        "stipend": "₹20,000/month",
        "deadline": "2025-02-28",
        "experience_required": "0-1 years",
        "education_required": "B.Tech/M.Tech CSE",
        "description": "Research-focused role working with deep learning models in NLP and Computer Vision. Strong Python and PyTorch required.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Deep Learning", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "PyTorch", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "NLP", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "Computer Vision", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "NumPy", "category": "skill", "mandatory": True, "importance": 0.7},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 1.0},
            {"requirement": "0-1 years", "category": "experience", "mandatory": False, "importance": 0.5},
        ],
    },
    {
        "company": "Insight Analytics",
        "title": "Data Science Intern",
        "domain": "Data Science",
        "location": "Hyderabad",
        "work_mode": "hybrid",
        "duration": "3 months",
        "stipend": "₹12,000/month",
        "deadline": "2025-03-01",
        "experience_required": "Freshers",
        "education_required": "B.Tech/BCA/B.Sc",
        "description": "Work on data pipelines, EDA, and ML model development. Python, Pandas, SQL required.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "SQL", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Pandas", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Machine Learning", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "Tableau", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "B.Tech", "category": "education", "mandatory": False, "importance": 0.7},
            {"requirement": "Freshers", "category": "experience", "mandatory": False, "importance": 0.5},
        ],
    },
    {
        "company": "ClearML",
        "title": "MLOps Intern",
        "domain": "AI/ML",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹18,000/month",
        "deadline": "2025-02-20",
        "experience_required": "0-1 years",
        "education_required": "B.Tech CSE",
        "description": "Help automate ML model deployment pipelines. Docker, Python, REST API, and basic ML knowledge required.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Docker", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "REST API", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Machine Learning", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "Linux", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "Git", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 0.9},
        ],
    },

    # ── Web Development ───────────────────────────────────────────────────────
    {
        "company": "Webcraft Studio",
        "title": "Frontend Developer Intern",
        "domain": "Web Development",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹10,000/month",
        "deadline": "2025-03-15",
        "experience_required": "Freshers",
        "education_required": "Any degree",
        "description": "Build beautiful, responsive UIs using React and Tailwind CSS. HTML/CSS/JS proficiency required.",
        "requirements": [
            {"requirement": "React", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "JavaScript", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "HTML", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "CSS", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "Tailwind", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "Git", "category": "skill", "mandatory": True, "importance": 0.7},
            {"requirement": "Figma", "category": "skill", "mandatory": False, "importance": 0.5},
        ],
    },
    {
        "company": "NextGen Apps",
        "title": "Full Stack Intern (React + Node)",
        "domain": "Web Development",
        "location": "Pune",
        "work_mode": "onsite",
        "duration": "6 months",
        "stipend": "₹15,000/month",
        "deadline": "2025-02-28",
        "experience_required": "0-1 years",
        "education_required": "B.Tech/BCA",
        "description": "Work on full-stack features using React (frontend) and Node.js/Express (backend). REST API integration required.",
        "requirements": [
            {"requirement": "React", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Node.js", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "JavaScript", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "REST API", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "SQL", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "MongoDB", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "B.Tech", "category": "education", "mandatory": False, "importance": 0.7},
        ],
    },
    {
        "company": "BluePixel",
        "title": "UI/UX Design Intern",
        "domain": "UI/UX",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹8,000/month",
        "deadline": "2025-03-31",
        "experience_required": "Freshers",
        "education_required": "Any",
        "description": "Create wireframes, prototypes, and high-fidelity designs using Figma. Design portfolio required.",
        "requirements": [
            {"requirement": "Figma", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "UI/UX", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "HTML", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "CSS", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "Adobe XD", "category": "skill", "mandatory": False, "importance": 0.4},
        ],
    },

    # ── Backend Development ───────────────────────────────────────────────────
    {
        "company": "CloudBridge Systems",
        "title": "Backend Developer Intern",
        "domain": "Backend Development",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹12,000/month",
        "deadline": "2025-02-28",
        "experience_required": "Freshers",
        "education_required": "B.Tech/BCA/MCA",
        "description": "Build and maintain REST APIs using Python FastAPI or Java Spring Boot. SQL database required.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": False, "importance": 0.8},
            {"requirement": "Java", "category": "skill", "mandatory": False, "importance": 0.8},
            {"requirement": "REST API", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "SQL", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Git", "category": "skill", "mandatory": True, "importance": 0.7},
            {"requirement": "Docker", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "B.Tech", "category": "education", "mandatory": False, "importance": 0.7},
        ],
    },
    {
        "company": "SpringStack",
        "title": "Java Backend Intern",
        "domain": "Backend Development",
        "location": "Bangalore",
        "work_mode": "hybrid",
        "duration": "6 months",
        "stipend": "₹18,000/month",
        "deadline": "2025-02-20",
        "experience_required": "0-1 years",
        "education_required": "B.Tech CSE/IT",
        "description": "Work on Java microservices using Spring Boot. Strong OOP and SQL knowledge required.",
        "requirements": [
            {"requirement": "Java", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Spring Boot", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "SQL", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "REST API", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Maven", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "Docker", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 0.9},
        ],
    },

    # ── Data Analytics ────────────────────────────────────────────────────────
    {
        "company": "VisuData Corp",
        "title": "Data Analytics Intern",
        "domain": "Data Analytics",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹10,000/month",
        "deadline": "2025-03-10",
        "experience_required": "Freshers",
        "education_required": "B.Tech/BCA/B.Sc",
        "description": "Perform data analysis, create dashboards in Power BI and Tableau, and write SQL queries for business insights.",
        "requirements": [
            {"requirement": "SQL", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Power BI", "category": "skill", "mandatory": False, "importance": 0.8},
            {"requirement": "Tableau", "category": "skill", "mandatory": False, "importance": 0.8},
            {"requirement": "Excel", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Python", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "Pandas", "category": "skill", "mandatory": False, "importance": 0.6},
        ],
    },
    {
        "company": "MetriX Analytics",
        "title": "Business Intelligence Intern",
        "domain": "Data Analytics",
        "location": "Mumbai",
        "work_mode": "hybrid",
        "duration": "3 months",
        "stipend": "₹12,000/month",
        "deadline": "2025-03-20",
        "experience_required": "Freshers",
        "education_required": "B.Tech/MBA/B.Sc",
        "description": "Work with BI tools to create KPI dashboards and reports. SQL and Excel mandatory.",
        "requirements": [
            {"requirement": "SQL", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Excel", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Power BI", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Tableau", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "Python", "category": "skill", "mandatory": False, "importance": 0.5},
        ],
    },

    # ── Cloud ─────────────────────────────────────────────────────────────────
    {
        "company": "SkyOps Cloud",
        "title": "Cloud Engineering Intern",
        "domain": "Cloud",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹14,000/month",
        "deadline": "2025-03-01",
        "experience_required": "Freshers",
        "education_required": "B.Tech CSE/ECE",
        "description": "Deploy and manage applications on AWS. Docker, Linux, and basic networking knowledge required.",
        "requirements": [
            {"requirement": "AWS", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Docker", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Linux", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "Python", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "CI/CD", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 0.9},
        ],
    },
    {
        "company": "NimbusTech",
        "title": "DevOps Intern",
        "domain": "Cloud",
        "location": "Bangalore",
        "work_mode": "onsite",
        "duration": "6 months",
        "stipend": "₹20,000/month",
        "deadline": "2025-02-15",
        "experience_required": "0-1 years",
        "education_required": "B.Tech CSE",
        "description": "Work on CI/CD pipelines, Docker containerization, and Kubernetes orchestration.",
        "requirements": [
            {"requirement": "Docker", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Kubernetes", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "CI/CD", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Linux", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "AWS", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "Python", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 0.9},
        ],
    },

    # ── Cybersecurity ─────────────────────────────────────────────────────────
    {
        "company": "SecureNet Labs",
        "title": "Cybersecurity Intern",
        "domain": "Cybersecurity",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹12,000/month",
        "deadline": "2025-03-15",
        "experience_required": "Freshers",
        "education_required": "B.Tech CSE/ECE",
        "description": "Learn and assist in vulnerability assessments, penetration testing, and security auditing. Linux and networking required.",
        "requirements": [
            {"requirement": "Linux", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Python", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "SQL", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 0.9},
            {"requirement": "Freshers", "category": "experience", "mandatory": False, "importance": 0.5},
        ],
    },
    {
        "company": "Fortress Security",
        "title": "Application Security Intern",
        "domain": "Cybersecurity",
        "location": "Hyderabad",
        "work_mode": "hybrid",
        "duration": "6 months",
        "stipend": "₹16,000/month",
        "deadline": "2025-02-28",
        "experience_required": "0-1 years",
        "education_required": "B.Tech CSE",
        "description": "Assist in SAST, DAST, and code security reviews. Python scripting and web development knowledge helpful.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Linux", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "JavaScript", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "SQL", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 1.0},
        ],
    },

    # ── Mobile / Android ──────────────────────────────────────────────────────
    {
        "company": "AppForge",
        "title": "Android Developer Intern",
        "domain": "Mobile Development",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹12,000/month",
        "deadline": "2025-03-10",
        "experience_required": "Freshers",
        "education_required": "B.Tech/BCA",
        "description": "Build Android applications using Java or Kotlin. REST API integration required.",
        "requirements": [
            {"requirement": "Java", "category": "skill", "mandatory": False, "importance": 0.8},
            {"requirement": "REST API", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "SQL", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "Git", "category": "skill", "mandatory": True, "importance": 0.7},
            {"requirement": "B.Tech", "category": "education", "mandatory": False, "importance": 0.7},
        ],
    },

    # ── More ML/AI ────────────────────────────────────────────────────────────
    {
        "company": "VisionAI",
        "title": "Computer Vision Intern",
        "domain": "AI/ML",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹15,000/month",
        "deadline": "2025-03-01",
        "experience_required": "Freshers",
        "education_required": "B.Tech CSE",
        "description": "Work on image recognition and object detection using deep learning. Python and OpenCV experience helpful.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Computer Vision", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Deep Learning", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "NumPy", "category": "skill", "mandatory": True, "importance": 0.7},
            {"requirement": "PyTorch", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 0.9},
        ],
    },
    {
        "company": "LangAI",
        "title": "NLP Engineer Intern",
        "domain": "AI/ML",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "6 months",
        "stipend": "₹18,000/month",
        "deadline": "2025-02-28",
        "experience_required": "0-1 years",
        "education_required": "B.Tech/M.Tech CSE",
        "description": "Build NLP pipelines for text classification, named entity recognition, and summarization.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "NLP", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Machine Learning", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "PyTorch", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "Pandas", "category": "skill", "mandatory": True, "importance": 0.7},
            {"requirement": "REST API", "category": "skill", "mandatory": False, "importance": 0.5},
        ],
    },
    {
        "company": "QuantumAI",
        "title": "Generative AI Intern",
        "domain": "AI/ML",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "3 months",
        "stipend": "₹20,000/month",
        "deadline": "2025-03-15",
        "experience_required": "0-1 years",
        "education_required": "B.Tech CSE",
        "description": "Work with LLMs, prompt engineering, and RAG pipelines. Strong Python and NLP background needed.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "NLP", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Deep Learning", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "REST API", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "Docker", "category": "skill", "mandatory": False, "importance": 0.6},
        ],
    },

    # ── Data Engineering ──────────────────────────────────────────────────────
    {
        "company": "DataPipe Co",
        "title": "Data Engineering Intern",
        "domain": "Data Science",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "6 months",
        "stipend": "₹16,000/month",
        "deadline": "2025-03-01",
        "experience_required": "0-1 years",
        "education_required": "B.Tech CSE/IT",
        "description": "Build ETL pipelines using Python, Airflow, and SQL. Experience with cloud storage a plus.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "SQL", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Pandas", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "Airflow", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "AWS", "category": "skill", "mandatory": False, "importance": 0.5},
            {"requirement": "Docker", "category": "skill", "mandatory": False, "importance": 0.5},
        ],
    },

    # ── SDE / General ─────────────────────────────────────────────────────────
    {
        "company": "BuildFast",
        "title": "Software Development Intern",
        "domain": "Software Development",
        "location": "Noida",
        "work_mode": "hybrid",
        "duration": "3 months",
        "stipend": "₹14,000/month",
        "deadline": "2025-02-28",
        "experience_required": "Freshers",
        "education_required": "B.Tech CSE",
        "description": "Generalist SDE role working across frontend and backend. Any major language acceptable.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "Java", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "JavaScript", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "SQL", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "Git", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "REST API", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 0.9},
        ],
    },
    {
        "company": "TechVenture",
        "title": "Product Engineering Intern",
        "domain": "Software Development",
        "location": "Delhi",
        "work_mode": "onsite",
        "duration": "3 months",
        "stipend": "₹10,000/month",
        "deadline": "2025-03-31",
        "experience_required": "Freshers",
        "education_required": "B.Tech/BCA",
        "description": "Work across product and engineering. Prototype features, write tests, and contribute to code reviews.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "JavaScript", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "Git", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "SQL", "category": "skill", "mandatory": False, "importance": 0.6},
            {"requirement": "REST API", "category": "skill", "mandatory": False, "importance": 0.5},
        ],
    },

    # ── Research ──────────────────────────────────────────────────────────────
    {
        "company": "AcademiX Research",
        "title": "AI Research Intern",
        "domain": "AI/ML",
        "location": "Remote",
        "work_mode": "remote",
        "duration": "6 months",
        "stipend": "₹15,000/month",
        "deadline": "2025-03-15",
        "experience_required": "0-1 years",
        "education_required": "B.Tech/M.Tech CSE",
        "description": "Contribute to research in reinforcement learning and autonomous agents. Strong math and Python required.",
        "requirements": [
            {"requirement": "Python", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Machine Learning", "category": "skill", "mandatory": True, "importance": 1.0},
            {"requirement": "Deep Learning", "category": "skill", "mandatory": True, "importance": 0.9},
            {"requirement": "NumPy", "category": "skill", "mandatory": True, "importance": 0.8},
            {"requirement": "PyTorch", "category": "skill", "mandatory": False, "importance": 0.7},
            {"requirement": "B.Tech", "category": "education", "mandatory": True, "importance": 1.0},
        ],
    },
]


def seed_database(db: Session):
    """Load sample data if the database is empty."""
    existing_students = db.query(Student).count()
    existing_internships = db.query(Internship).count()

    if existing_students == 0:
        for s_data in SAMPLE_STUDENTS:
            skills = s_data.pop("skills", [])
            projects = s_data.pop("projects", [])
            student = Student(**s_data)
            db.add(student)
            db.flush()

            for sk in skills:
                db.add(StudentSkill(student_id=student.id, **sk))
            for pr in projects:
                db.add(Project(student_id=student.id, **pr))

        db.commit()
        print(f"✓ Seeded {len(SAMPLE_STUDENTS)} sample students")

    if existing_internships == 0:
        for i_data in SAMPLE_INTERNSHIPS:
            reqs = i_data.pop("requirements", [])
            internship = Internship(is_sample=True, **i_data)
            db.add(internship)
            db.flush()

            for r in reqs:
                db.add(InternshipRequirement(internship_id=internship.id, **r))

        db.commit()
        print(f"✓ Seeded {len(SAMPLE_INTERNSHIPS)} sample internships")
