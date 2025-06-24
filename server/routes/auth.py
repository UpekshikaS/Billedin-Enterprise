# server/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import psycopg2, bcrypt
from psycopg2.extras import RealDictCursor
from routes.auth import auth

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    try:
        conn = psycopg2.connect(
            dbname="billedin_db",
            user="your_db_user",
            password="your_db_pass",
            host="localhost",
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            token = create_access_token(identity={"id": user['id'], "role": user['role']})
            return jsonify({"token": token}), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401

    except Exception as e:
        print("Login Error:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        if conn:
            cur.close()
            conn.close()
