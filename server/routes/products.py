# server/routes/products.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import psycopg2
from psycopg2.extras import RealDictCursor
from middleware.subscription_check import subscription_required

@products.route('/api/products', methods=['GET'])
@jwt_required()
@subscription_required
def get_products():
    ...


products = Blueprint('products', __name__)

@products.route('/api/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        conn = psycopg2.connect(
            dbname="billedin_db",
            user="postgres",
            password="Earth@123#456",
            host="localhost",
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        return jsonify(rows), 200

    except Exception as e:
        print("Get Products Error:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        if conn:
            cur.close()
            conn.close()
