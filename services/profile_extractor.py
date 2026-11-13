import re


def extract_candidate_profile(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = None

    if lines and re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,80}", lines[0]):
        name = lines[0].title()

    email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", text)

    phone_match = re.search(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
        text,
    )

    linkedin_match = re.search(
        r"https?://(?:www\.)?linkedin\.com/[^\s|]+",
        text,
    )

    return {
        "name": name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "linkedin": linkedin_match.group(0).rstrip(".,;)")
        if linkedin_match
        else None,
    }