from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extension import db
from app.models.category import Category


# Create Category
categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

@categories_bp.route("/", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"})
    
    name = data.get("name")

    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    existing = Category.query.filter_by(name=name).first()

    if existing:
        return jsonify({"error": "Category with this name already exists"}), 409

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category created successfully", "category": new_category.to_dict()}), 201

# Get All Categories
@categories_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()

    return jsonify({"categories": [category.to_dict() for category in categories]}), 200