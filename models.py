
from extensions import db


class AnalysisHistory(db.Model):

    __tablename__ = "analysis_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    analysis_type = db.Column(db.String(50))
    resume_filename = db.Column(db.String(255))

    candidate_name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(30))

    resume_score = db.Column(db.Numeric(5, 2))
    semantic_score = db.Column(db.Numeric(5, 2), nullable=True)

    job_description = db.Column(db.Text)
    matching_skills = db.Column(db.Text)
    missing_skills = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    detected_sections = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )
