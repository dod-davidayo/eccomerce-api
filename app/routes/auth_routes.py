from flask import Blueprint, request, jsonify
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash   #for password hashing
import re # regular expression module for passwor validation
from app.extension import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token


#routes for authentication (register, login, protected route)
auth_rt = Blueprint("auth", __name__, url_prefix="/auth")
 

# register route
@auth_rt.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error":"No input data provided"}), 400
    email = data.get("email")
    password = data.get("password")

    # check if any field is empty
    if not email or not password:
        return jsonify({"error": "email, and password are required"}), 400
    
    # check if user already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:

        return jsonify({
            "error": "User already exists"
        }), 409
    
    # check if email is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email address"}), 400
    
    

    # hash password
    hashed_password = generate_password_hash(password)

    # create new user
    new_user = User(email=email, password_hash=hashed_password, user_role='user')

    # save user to database
    db.session.add(new_user)
    db.session.commit()

    # return success message
    return jsonify({"message": "User registered successfully"}), 201

# login route
@auth_rt.route("/login", methods=["POST"])
def login():
    data = request.get_json() # get JSON data from request
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    email = data.get("email") # get email from data
    password = data.get("password") # get password from data

    # check if email and password are provided
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # find user
    existing_user = User.query.filter_by(email=email).first()


    # if user not found or password is incorrect, return error
    if not existing_user or not check_password_hash(existing_user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401
    

    
    # create access token/ refresh token and return it to the client
    access_token = create_access_token(identity=str(existing_user.id))
    refresh_token = create_refresh_token(identity=str(existing_user.id))
    return jsonify({"Message": "Login successful", 
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user_id": existing_user.to_dict()}), 200

# auth profile code has not upated 


    

# protected route
@auth_rt.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = int(get_jwt_identity()) # get user id from token
    user = db.session.get(User, current_user_id) # get user from database
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": f"Hello, {user.username}! This is a protected route."}), 200

