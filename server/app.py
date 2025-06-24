# auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import psycopg2
import bcrypt
import os

auth = Blueprint('auth', __name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="billedin_db",
        user="your_db_user",
        password="your_db_password",
        host="localhost"
    )

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, password, full_name, role, subscription_active FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    user_id, user_email, password_hash, full_name, role, is_active = user

    if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
        return jsonify({"message": "Invalid email or password"}), 401

    if not is_active:
        return jsonify({"message": "Subscription is inactive"}), 403

    access_token = create_access_token(identity={
        "id": user_id,
        "email": user_email,
        "role": role,
        "name": full_name
    })

    return jsonify(access_token=access_token), 200
