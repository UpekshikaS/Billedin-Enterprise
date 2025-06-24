from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.subscription_check import subscription_required
import psycopg2

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
