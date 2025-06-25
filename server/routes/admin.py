from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.decorators import admin_required
from database.connection import get_db


admin = Blueprint('admin', __name__)

@admin.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_users():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403
    # fetch users logic here...
    return jsonify(users), 200

@admin.route('/api/admin/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    cur = get_db().cursor()
    cur.execute("SELECT id, full_name, email, role, subscription_active FROM users")
    rows = cur.fetchall()
    cur.close()

    users = [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "role": row[3],
            "subscription_active": row[4]
        } for row in rows
    ]

    return jsonify(users), 200

@admin.route('/api/admin/users/<int:user_id>/subscription', methods=['PUT'])
@jwt_required()
@admin_required
def update_subscription(user_id):
    data = request.get_json()
    status = data.get("subscription_active")

    cur = get_db().cursor()
    cur.execute("UPDATE users SET subscription_active = %s WHERE id = %s", (status, user_id))
    get_db().commit()
    cur.close()

    return jsonify({"message": "Subscription updated."}), 200