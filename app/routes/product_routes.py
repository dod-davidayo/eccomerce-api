from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product import Product
from app.extension import db

products_bp = Blueprint("products", __name__, url_prefix="/products")

# Create Products
@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock_quantity = data.get("stock_quantity")
    category_id = data.get("category_id")

    if (not name or not description or price is None or stock_quantity is None or category_id is None
):
        return jsonify({"error": "All fields are required"}), 400
    existing_product = Product.query.filter_by(name=name).first()
    if existing_product:
        return jsonify({"error": "Product with this name already exists"}), 409
    
    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        category_id=category_id
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created successfully", "product": new_product.to_dict()}), 201

# get all products
@products_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

# get product by id
@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict()), 200

# Update product 
@products_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock_quantity = data.get("stock_quantity")
    category_id = data.get("category_id")

    if name:
        product.name = name
    if description:
        product.description = description
    if price:
        product.price = price
    if stock_quantity:
        product.stock_quantity = stock_quantity
    if category_id:
        product.category_id = category_id

    db.session.commit()

    return jsonify({"message": "Product updated successfully", "product": product.to_dict()}), 200

# delete product
@products_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200
