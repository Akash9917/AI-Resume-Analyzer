SECTION_WEIGHTS = {
    "Education": 10,
    "Projects": 30,
    "Experience": 20,
}


def calculate_resume_strength(skills, sections):
    skills_score = min(len(skills) * 4, 40)

    found_sections = {
        section["name"]
        for section in sections
        if section["found"]
    }

    sections_score = sum(
        points
        for section_name, points in SECTION_WEIGHTS.items()
        if section_name in found_sections
    )

    score = skills_score + sections_score

    if score >= 80:
        feedback = "Strong resume foundation. Add measurable achievements to improve further."
    elif score >= 60:
        feedback = "Good start. Add missing sections or more relevant skills."
    else:
        feedback = "Build your resume by adding skills, projects, and relevant sections."

    return {
        "score": score,
        "feedback": feedback,
        "breakdown": [
            {"label": "Detected skills", "points": skills_score, "maximum": 40},
            {"label": "Resume sections", "points": sections_score, "maximum": 60},
        ],
    }