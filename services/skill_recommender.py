SKILL_RECOMMENDATIONS = {
    "Python": "Practice Python basics and add one Python project to your resume.",
    "SQL": "Practice SELECT, JOIN, and GROUP BY queries.",
    "HTML": "Build a responsive webpage and add it to your portfolio.",
    "CSS": "Improve a project with responsive layouts and clean styling.",
    "JavaScript": "Build an interactive webpage using DOM manipulation.",
    "Flask": "Build a small Flask CRUD project and add its GitHub link.",
    "Git": "Use Git commits in your projects and mention version control.",
    "GitHub": "Upload your best projects with clear README files.",
    "Machine Learning": "Complete one ML prediction project using a public dataset.",
    "Deep Learning": "Build a beginner neural-network project.",
    "Generative AI": "Create a small Generative AI project.",
    "Data Analysis": "Analyze a dataset and show insights with charts.",
    "Pandas": "Practice cleaning and analyzing CSV data with Pandas.",
    "NumPy": "Practice arrays and numerical operations with NumPy.",
    "MySQL": "Create a small MySQL database project.",
    "MongoDB": "Build a CRUD project that stores data in MongoDB.",
}


def get_skill_recommendations(skills):
    return [
        {
            "skill": skill,
            "suggestion": SKILL_RECOMMENDATIONS.get(
                skill,
                f"Learn the basics of {skill} and add a related project.",
            ),
        }
        for skill in skills
    ]