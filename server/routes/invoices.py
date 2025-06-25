from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2

from middleware.subscription_check import subscription_required  # Ensure this is the correct path

invoices = Blueprint('invoices', __name__)

@invoices.route('/api/invoices', methods=['POST'])
@jwt_required()
@subscription_required  # ✅ Subscription check added here
def create_invoice():
    user = get_jwt_identity()
    data = request.get_json()
    items = data.get('items')
    total_amount = data.get('total_amount')

    if not items or total_amount is None:
        return jsonify({"message": "Invalid invoice data"}), 400

    try:
        conn = psycopg2.connect(
            dbname="billedin_db",
            user="postgres",
            password="Earth@123#456",
            host="localhost"
        )
        cur = conn.cursor()

        # Insert invoice
        cur.execute(
            "INSERT INTO invoices (user_id, total_amount) VALUES (%s, %s) RETURNING id",
            (user['id'], total_amount)
        )
        invoice_id = cur.fetchone()[0]

        # Insert invoice items
        for item in items:
            cur.execute(
                "INSERT INTO invoice_items (invoice_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (invoice_id, item['productId'], item['quantity'], item['price'])
            )

        conn.commit()
        return jsonify({"message": "Invoice created", "invoice_id": invoice_id}), 201

    except Exception as e:
        print("Create Invoice Error:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        if conn:
            cur.close()
            conn.close()
