import re


KNOWN_SKILLS = (
    "Python",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Flask",
    "Git",
    "GitHub",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "MySQL",
    "MongoDB",
    "Power BI",
    "Excel",
)


def extract_skills(text):
    return [
        skill
        for skill in KNOWN_SKILLS
        if re.search(rf"(?<!\w){re.escape(skill)}(?!\w)", text, re.IGNORECASE)
    ]