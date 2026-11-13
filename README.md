# AI-Based Resume Analyzer & Job Matching System



A Flask-based web application that analyzes resumes, extracts candidate information and skills, evaluates resume strength, and matches candidate skills against job descriptions.



## Features



- PDF resume upload and text extraction

- Candidate profile extraction

- Technical skill detection

- Resume section detection

- Rule-based resume strength scoring

- Job description skill matching

- Missing skill identification

- Skill improvement recommendations

- Analysis history and dashboard

- Search and filter analysis history

- CSV export

- Downloadable PDF analysis reports



## Technology Stack



- Python

- Flask

- HTML, CSS, Bootstrap 5, JavaScript

- MySQL

- Flask-SQLAlchemy

- PyMuPDF

- ReportLab

- Chart.js



## Installation and Setup



### 1. Clone the repository



```bash

git clone https://github.com/Akash9917/AI-Resume-Analyzer.git

cd AI-Resume-Analyzer

```



### 2. Create and activate virtual environment



```powershell

python -m venv venv

.\venv\Scripts\Activate.ps1

```



### 3. Install dependencies



```bash

python -m pip install -r requirements.txt

```



### 4. Configure MySQL



Create a database named `ai_resume_analyzer`.



Create a `.env` file in the project root:



```env

DB_USER=resume_app

DB_PASSWORD=your_database_password

DB_HOST=localhost

DB_PORT=3306

DB_NAME=ai_resume_analyzer

SECRET_KEY=your_secret_key

```



### 5. Run the application



```bash

python app.py

```



Open your browser:



http://127.0.0.1:5000



## Important Notes



- Never upload your `.env` file or database credentials.

- Uploaded resumes may contain personal information. Keep them private.

- Resume scoring and skill matching currently use rule-based logic and a curated skill dictionary.

- Scanned image-based PDFs are not supported by the current text extraction implementation.



## Future Enhancements



- Advanced NLP-based skill extraction

- Semantic resume and job description matching

- Improved job-specific resume evaluation

- AI-powered career recommendations



## License



This project is developed for academic and educational purposes.

