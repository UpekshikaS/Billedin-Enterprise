from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.subscription_check import subscription_required
import psycopg2
from database.connection import get_db

stats = Blueprint('stats', __name__)

@stats.route('/api/stats/summary', methods=['GET'])
@jwt_required()
@subscription_required
def get_summary():
    user = get_jwt_identity()
    try:
        conn = psycopg2.connect(
            dbname="billedin_db",
            user="postgres",
            password="yEarth@123#456",
            host="localhost"
        )
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM invoices WHERE user_id = %s", (user['id'],))
        count, total = cur.fetchone()

        return jsonify({
            "invoice_count": count,
            "total_revenue": float(total)
        })
    except Exception as e:
        print("Stats Error:", e)
        return jsonify({ "message": "Error fetching stats" }), 500
    finally:
        if conn:
            cur.close()
            conn.close()


@stats.route('/api/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    identity = get_jwt_identity()
    role = identity.get("role")
    user_id = identity.get("id")

    cur = get_db().cursor()

    if role == 'admin':
        cur.execute("SELECT COUNT(*) FROM invoices")
        invoice_count = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(total), 0) FROM invoices")
        total_revenue = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM products")
        product_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]

    else:
        cur.execute("SELECT COUNT(*) FROM invoices WHERE user_id = %s", (user_id,))
        invoice_count = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(total), 0) FROM invoices WHERE user_id = %s", (user_id,))
        total_revenue = cur.fetchone()[0]

        product_count = None
        user_count = None

    cur.close()

    return jsonify({
        "invoice_count": invoice_count,
        "total_revenue": float(total_revenue),
        "product_count": product_count,
        "user_count": user_count
    })
