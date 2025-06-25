from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
from database.connection import get_db

def subscription_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        user_id = identity.get("id")

        cur = get_db().cursor()
        cur.execute("SELECT subscription_active FROM users WHERE id = %s", (user_id,))
        result = cur.fetchone()
        cur.close()

        if not result or result[0] is False:
            return jsonify({"message": "Your subscription has expired. Please contact admin."}), 403

        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity.get("role") != "admin":
            return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper