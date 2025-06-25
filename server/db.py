import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("localhost"),
        database=os.getenv("billedin"),
        user=os.getenv("postgres"),
        password=os.getenv("Earth@123#456"),
    )

