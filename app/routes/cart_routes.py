from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extension import db
from app.models.cart import Cart
from app.models.product import Product

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


#add cart
@cart_bp.route("/", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    # check if item already exists
    cart_item = Cart.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if cart_item:
        # update quantity instead of inserting duplicate
        cart_item.quantity += quantity
    else:
        # create new cart item
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        "message": "Product added to cart successfully",
        "cart_item": cart_item.to_dict()
    }), 201

    
# view cart items
@cart_bp.route("/", methods=["GET"])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    return jsonify({"cart_items": [item.to_dict() for item in cart_items]}), 200

# Remove item from cart
@cart_bp.route("/<int:cart_item_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(cart_item_id):
    user_id = get_jwt_identity()
    cart_item = Cart.query.filter_by(id=cart_item_id, user_id=user_id).first()

    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404
    
    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Cart item removed successfully"}), 200 

