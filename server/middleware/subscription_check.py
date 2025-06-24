from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
import psycopg2

def subscription_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        try:
            conn = psycopg2.connect(
                dbname="billedin_db",
                user="your_db_user",
                password="your_db_pass",
                host="localhost"
            )
            cur = conn.cursor()
            cur.execute("SELECT subscription_active FROM users WHERE id = %s", (user['id'],))
            active = cur.fetchone()
            if not active or not active[0]:
                return jsonify({"message": "Subscription inactive. Please renew."}), 403
        except Exception as e:
            print("Subscription check error:", e)
            return jsonify({"message": "Server error"}), 500
        finally:
            if conn:
                cur.close()
                conn.close()
        return fn(*args, **kwargs)
    return wrapper
