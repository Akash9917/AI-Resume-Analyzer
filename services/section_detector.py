import re


SECTION_PATTERNS = {
    "Education": r"^\s*(education|academic background|qualifications?)\s*$",
    "Projects": r"^\s*(projects?|personal projects?|academic projects?)\s*$",
    "Experience": (
        r"^\s*(experience|work experience|professional experience|"
        r"employment|internships?)\s*$"
    ),
}


def detect_resume_sections(text):
    return [
        {
            "name": name,
            "found": bool(re.search(pattern, text, re.IGNORECASE | re.MULTILINE)),
        }
        for name, pattern in SECTION_PATTERNS.items()
    ]