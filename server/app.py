
# from flask import Flask
# from flask_cors import CORS
# from flask_jwt_extended import JWTManagerfrom flask import Blueprint, request, jsonify
# from flask_jwt_extended import create_access_token
# import psycopg2
# import bcrypt

# # auth = Blueprint('auth', __name__)
# app = Flask(__name__)
# CORS(
#     app,
#     resources={r"/api/*": {"origins": "http://localhost:3000"}},
#     supports_credentials=True,
#     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#     allow_headers=["Content-Type", "Authorization"]
# )


# def get_db_connection():
#     return psycopg2.connect(
#         dbname="billedin_db",
#         user="postgres",
#         password="Earth@123#456",
#         host="localhost"
#     )

# @auth.route('/api/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     if not email or not password:
#         return jsonify({"message": "Email and password are required"}), 400

#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT id, email, password, full_name, role, subscription_active FROM users WHERE email = %s", (email,))
#     user = cur.fetchone()
#     cur.close()
#     conn.close()

#     if not user:
#         return jsonify({"message": "Invalid email or password"}), 401

#     user_id, user_email, password_hash, full_name, role, is_active = user

#     if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
#         return jsonify({"message": "Invalid email or password"}), 401

#     if not is_active:
#         return jsonify({"message": "Subscription is inactive"}), 403

#     access_token = create_access_token(identity={
#         "id": user_id,
#         "email": user_email,
#         "role": role,
#         "name": full_name
#     })

#     return jsonify(access_token=access_token), 200
# app.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

from auth import auth
from routes.invoices import invoices
from routes.stats import stats
from routes.admin import admin
app.register_blueprint(admin)

load_dotenv()

app = Flask(__name__)

CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:3000"}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret')
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(admin)
app.register_blueprint(stats)
app.register_blueprint(invoices)
app.register_blueprint(auth)

@app.route("/")
def home():
    return {"message": "BilledIn Backend is Running"}

if __name__ == "__main__":
    app.run(debug=True)
