from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import psycopg2, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # validate and return JWT token
