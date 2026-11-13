
import os
import csv
import io
import json

from flask import Flask, render_template, request, send_file, make_response
from werkzeug.utils import secure_filename

from config import Config
from extensions import db
from models import AnalysisHistory

from services.resume_scorer import calculate_resume_strength
from services.profile_extractor import extract_candidate_profile
from services.skill_recommender import get_skill_recommendations
from services.section_detector import detect_resume_sections
from services.pdf_extractor import extract_text_from_pdf
from services.skill_extractor import extract_skills
from services.skill_matcher import calculate_skill_match
from services.report_generator import generate_analysis_report


# -----------------------------------------
# FLASK APPLICATION CONFIGURATION
# -----------------------------------------

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------------------
# FILE VALIDATION
# -----------------------------------------

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# -----------------------------------------
# HOME PAGE
# -----------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------------------
# RESUME UPLOAD AND ANALYSIS
# -----------------------------------------

@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():

    if request.method == "POST":

        if "resume" not in request.files:
            return "No file selected.", 400

        file = request.files["resume"]

        if file.filename == "":
            return "Please select a PDF file.", 400

        if not allowed_file(file.filename):
            return "Invalid file! Please upload a PDF.", 400

        # Validate file size (Maximum 5 MB)
        file.stream.seek(0, os.SEEK_END)
        file_size = file.stream.tell()
        file.stream.seek(0)

        max_size = 5 * 1024 * 1024

        if file_size == 0:
            return "The uploaded file is empty.", 400

        if file_size > max_size:
            return "File size exceeds 5 MB. Please upload a smaller PDF.", 400

        filename = secure_filename(file.filename)

        if not filename:
            return "Invalid filename.", 400

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(file_path)

        # Extract PDF text
        try:

            extracted_text = extract_text_from_pdf(file_path)

        except ValueError as error:

            return str(error), 400

        if not extracted_text.strip():
            return "No readable text found in this PDF.", 400

        # Extract resume information
        skills = extract_skills(extracted_text)

        sections = detect_resume_sections(extracted_text)

        resume_strength = calculate_resume_strength(
            skills,
            sections
        )

        profile = extract_candidate_profile(extracted_text)

        # Save analysis in MySQL
        try:

            history = AnalysisHistory(

                analysis_type="resume_analysis",

                resume_filename=filename,

                candidate_name=profile.get("name", ""),

                email=profile.get("email", ""),

                phone=profile.get("phone", ""),

                resume_score=resume_strength.get("score", 0),

                matching_skills=json.dumps(skills),

                missing_skills=json.dumps([]),

                recommendations=json.dumps([]),

                detected_sections=json.dumps(sections)
            )

            db.session.add(history)

            db.session.commit()

        except Exception:

            db.session.rollback()

            raise

        # Display analysis result
        return render_template(

            "analysis_result.html",

            filename=filename,

            preview=extracted_text[:1000],

            skills=skills,

            sections=sections,

            resume_strength=resume_strength,

            profile=profile
        )

    return render_template("upload_resume.html")


# -----------------------------------------
# DOWNLOAD ANALYSIS REPORT
# -----------------------------------------

@app.route("/download-report", methods=["POST"])
def download_report():

    profile = {

        "name": request.form.get("profile_name"),

        "email": request.form.get("profile_email"),

        "phone": request.form.get("profile_phone"),

        "linkedin": request.form.get("profile_linkedin")
    }

    resume_strength = {

        "score": request.form.get("resume_score", "0"),

        "feedback": request.form.get("resume_feedback", "")
    }

    report = generate_analysis_report(

        profile,

        resume_strength,

        request.form.getlist("skills"),

        request.form.getlist("sections")
    )

    return send_file(

        report,

        as_attachment=True,

        download_name="resume_analysis_report.pdf",

        mimetype="application/pdf"
    )


# -----------------------------------------
# JOB DESCRIPTION SKILL MATCHING
# -----------------------------------------


@app.route("/match-skills", methods=["POST"])
def match_skills():

    job_description = request.form.get(
        "job_description", ""
    ).strip()

    resume_skills = request.form.getlist("resume_skills")

    if not job_description:
        return "Please paste a job description.", 400

    if not resume_skills:
        return "No resume skills provided.", 400

    job_skills = extract_skills(job_description)

    match_percentage, matching_skills, missing_skills = calculate_skill_match(
        resume_skills,
        job_skills
    )

    recommendations = get_skill_recommendations(
        missing_skills
    )

    # Save job matching result in MySQL
    history = AnalysisHistory(
        analysis_type="skill_matching",
        resume_filename=request.form.get("resume_filename", ""),
        resume_score=match_percentage,
        job_description=job_description,
        matching_skills=json.dumps(matching_skills),
        missing_skills=json.dumps(missing_skills),
        recommendations=json.dumps(recommendations)
    )

    try:
        db.session.add(history)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return render_template(
        "match_result.html",
        match_percentage=match_percentage,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        recommendations=recommendations
    )



# -----------------------------------------
# FILE SIZE ERROR HANDLER
# -----------------------------------------

@app.errorhandler(413)
def file_too_large(error):

    return "File too large! Maximum allowed size is 5 MB.", 413


# -----------------------------------------
# RUN APPLICATION
# -----------------------------------------

@app.route("/history")
def history():

    records = AnalysisHistory.query.order_by(
        AnalysisHistory.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        records=records
    )


@app.route("/dashboard")
def dashboard():

    total_analyses = AnalysisHistory.query.count()

    resume_count = AnalysisHistory.query.filter_by(
        analysis_type="resume_analysis"
    ).count()

    matching_count = AnalysisHistory.query.filter_by(
        analysis_type="skill_matching"
    ).count()

    average_score = db.session.query(
        db.func.avg(AnalysisHistory.resume_score)
    ).scalar() or 0

    resume_average = db.session.query(
        db.func.avg(AnalysisHistory.resume_score)
    ).filter_by(
        analysis_type="resume_analysis"
    ).scalar() or 0

    matching_average = db.session.query(
        db.func.avg(AnalysisHistory.resume_score)
    ).filter_by(
        analysis_type="skill_matching"
    ).scalar() or 0

    recent_analyses = AnalysisHistory.query.order_by(
        AnalysisHistory.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        total_analyses=total_analyses,
        resume_count=resume_count,
        matching_count=matching_count,
        average_score=average_score,
        resume_average=resume_average,
        matching_average=matching_average,
        recent_analyses=recent_analyses
    )


@app.route("/analysis-details/<int:analysis_id>")
def analysis_details(analysis_id):

    record = AnalysisHistory.query.get_or_404(analysis_id)

    return render_template(
        "analysis_details.html",
        record=record,
        matching_skills=json.loads(record.matching_skills or "[]"),
        missing_skills=json.loads(record.missing_skills or "[]"),
        recommendations=json.loads(record.recommendations or "[]"),
        sections=json.loads(record.detected_sections or "[]")
    )

@app.route("/export-history")
def export_history():

    records = AnalysisHistory.query.order_by(
        AnalysisHistory.created_at.desc()
    ).all()

    output = io.StringIO(newline="")
    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "ID",
        "Analysis Type",
        "Resume Filename",
        "Candidate Name",
        "Email",
        "Phone",
        "Score",
        "Job Description",
        "Matching Skills",
        "Missing Skills",
        "Recommendations",
        "Date"
    ])

    # CSV Data
    for record in records:
        writer.writerow([
            record.id,
            record.analysis_type,
            record.resume_filename,
            record.candidate_name,
            record.email,
            record.phone,
            record.resume_score,
            record.job_description,
            record.matching_skills,
            record.missing_skills,
            record.recommendations,
            record.created_at
        ])

    response = make_response(
        "\ufeff" + output.getvalue()
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=analysis_history.csv"
    )

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    return response

if __name__ == "__main__":

    app.run(debug=True)
