from flask import Blueprint,  jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extension import db
from app.models.order import Order


order_bp = Blueprint("orders", __name__, url_prefix="/orders")

# Create Order
@order_bp.route("/", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    new_order = Order(user_id=user_id)

    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order created successfully", "order": new_order.to_dict()}), 201    

# GET USER ORDERS
@order_bp.route("/", methods=["GET"])
@jwt_required
def get_orders():
    user_id = get_jwt_identity()

    orders = Order.query.filter_by(user_id=user_id).all()

    return jsonify({"orders": [order.to_dict() for order in orders]}), 200