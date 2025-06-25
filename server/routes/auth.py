# auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import psycopg2
import bcrypt

auth = Blueprint('auth', __name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="billedin_db",
        user="postgres",
        password="Earth@123#456",
        host="localhost"
    )

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, password, full_name, role, subscription_active FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    user_id, user_email, password_hash, full_name, role, subscription_active = user

    if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        return jsonify({"message": "Invalid email or password"}), 401

    if not subscription_active:
        return jsonify({"message": "Subscription inactive"}), 403

    access_token = create_access_token(identity={
        "id": user_id,
        "email": user_email,
        "role": role,
        "name": full_name
    })

    return jsonify(access_token=access_token), 200

# ✅ Register endpoint
@auth.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not all([email, password, name]):
        return jsonify({"message": "All fields are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"message": "Email already registered"}), 409

        cur.execute("""
            INSERT INTO users (email, password, full_name, role, subscription_active)
            VALUES (%s, %s, %s, %s, %s)
        """, (email, hashed_password, name, 'user', True))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        print("Registration Error:", e)
        return jsonify({"message": "Server error"}), 500
