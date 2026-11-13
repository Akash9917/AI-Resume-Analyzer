def calculate_skill_match(resume_skills, job_skills):
    resume_skill_set = set(resume_skills)

    matching_skills = [
        skill
        for skill in job_skills
        if skill in resume_skill_set
    ]

    missing_skills = [
        skill
        for skill in job_skills
        if skill not in resume_skill_set
    ]

    match_percentage = 0

    if job_skills:
        match_percentage = round(
            len(matching_skills) / len(job_skills) * 100
        )

    return match_percentage, matching_skills, missing_skills