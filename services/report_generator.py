from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_analysis_report(profile, resume_strength, skills, sections):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.textColor = colors.HexColor("#0d6efd")

    story = [
        Paragraph("AI Resume Analysis Report", title_style),
        Spacer(1, 16),
    ]

    story.append(Paragraph("Candidate Profile", styles["Heading2"]))

    for label, value in (
        ("Name", profile.get("name")),
        ("Email", profile.get("email")),
        ("Mobile", profile.get("phone")),
        ("LinkedIn", profile.get("linkedin")),
    ):
        if value:
            story.append(
                Paragraph(f"<b>{label}:</b> {escape(value)}", styles["BodyText"])
            )

    story.extend([
        Spacer(1, 14),
        Paragraph("Resume Strength", styles["Heading2"]),
        Paragraph(
            f"<b>Score:</b> {resume_strength['score']}/100",
            styles["BodyText"],
        ),
        Paragraph(resume_strength["feedback"], styles["BodyText"]),
        Spacer(1, 14),
        Paragraph("Detected Skills", styles["Heading2"]),
        Paragraph(
            ", ".join(skills) if skills else "No skills detected.",
            styles["BodyText"],
        ),
        Spacer(1, 14),
        Paragraph("Resume Sections", styles["Heading2"]),
    ])

    for section in sections:
        story.append(Paragraph(section, styles["BodyText"]))

    document.build(story)
    buffer.seek(0)

    return buffer