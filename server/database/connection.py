import psycopg2
import os

def get_db():
    return psycopg2.connect(
        dbname=os.getenv("billedin"),
        user=os.getenv("postgres"),
        password=os.getenv("Earth@123#456"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432)
    )
