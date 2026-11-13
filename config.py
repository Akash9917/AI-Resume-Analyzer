
import os
from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
secret_key = os.getenv("SECRET_KEY")

if not db_user:
    raise ValueError("DB_USER missing. Check your .env file.")

if not db_password:
    raise ValueError("DB_PASSWORD missing. Check your .env file.")

if not secret_key:
    raise ValueError("SECRET_KEY missing. Check your .env file.")


class Config:
    SECRET_KEY = secret_key

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "ai_resume_analyzer")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
