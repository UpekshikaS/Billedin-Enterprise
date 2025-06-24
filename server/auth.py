from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import get_db_connection
import bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password').encode('utf-8')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    user_id, hashed_pw = user
    if not bcrypt.checkpw(password, hashed_pw.encode('utf-8')):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"id": user_id, "email": email})
    return jsonify(access_token=access_token), 200
