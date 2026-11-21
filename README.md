# AI-Based Resume Analyzer & Job Matching System

An AI-powered web application built using Python and Flask that analyzes resumes, extracts candidate information and technical skills, evaluates resume strength, and matches candidate skills with job descriptions using keyword-based and semantic matching techniques.

## Features

### Resume Analysis
- PDF resume upload and text extraction
- Candidate profile extraction (Name, Email, Phone)
- Technical skill detection
- Resume section detection
- Rule-based resume strength scoring
- Skill improvement recommendations

### AI-Based Job Matching
- Job description skill extraction
- Keyword-based skill matching
- Missing skill identification
- AI-powered semantic similarity using MiniLM
- Separate keyword coverage and semantic similarity scores

### Dashboard & History
- Dashboard with analysis statistics
- Resume and job matching analytics
- Analysis history
- Search and filter analysis records
- Detailed analysis results
- CSV export
- Downloadable PDF analysis reports

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Database | MySQL |
| ORM | Flask-SQLAlchemy |
| PDF Processing | PyMuPDF |
| PDF Report Generation | ReportLab |
| Data Visualization | Chart.js |
| AI / NLP | MiniLM, ONNX Runtime |
| Version Control | Git and GitHub |

## System Architecture

The application follows a modular architecture:

1. **Frontend Layer:** Provides the user interface for uploading resumes, entering job descriptions, and viewing results.
2. **Flask Application Layer:** Handles requests, application routes, validation, and processing.
3. **Resume Processing Layer:** Extracts text, candidate details, skills, and resume sections.
4. **AI Matching Layer:** Performs keyword-based matching and semantic similarity analysis.
5. **Database Layer:** Stores analysis records and relevant results in MySQL.
6. **Reporting Layer:** Generates downloadable PDF reports and CSV exports.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Akash9917/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create and Activate Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure MySQL

Create a MySQL database named:

```sql
CREATE DATABASE ai_resume_analyzer;
```

Create a `.env` file in the project root:

```env
DB_USER=resume_app
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ai_resume_analyzer
SECRET_KEY=your_secret_key
```

Replace the example credentials with your actual local database configuration.

### 5. Download the AI Model

Download the required MiniLM model using:

```bash
python scripts/download_model.py
```

The model is stored locally and used for semantic similarity calculations.

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

## How the Matching System Works

The application uses two complementary matching techniques:

- **Keyword Skill Coverage:** Compares skills extracted from the resume with skills identified in the job description.
- **AI Semantic Similarity:** Uses MiniLM embeddings to measure the semantic similarity between resume content and job requirements.

These scores represent different measurements. Semantic similarity is not a prediction of hiring or shortlisting probability.

## Important Notes

- Never upload your `.env` file or database credentials to GitHub.
- Uploaded resumes may contain personal information and should be handled securely.
- Resume strength scoring uses rule-based evaluation.
- Semantic matching provides similarity estimates, not guaranteed recruitment outcomes.
- Scanned image-based PDFs may not be supported by the current text extraction implementation.
- The AI model must be downloaded before using semantic matching.

## Future Scope

- Advanced contextual resume evaluation
- Improved skill extraction and classification
- Job-specific resume improvement suggestions
- Integration with external job portals
- More comprehensive career recommendation features

## License

This project is developed for academic and educational purposes.