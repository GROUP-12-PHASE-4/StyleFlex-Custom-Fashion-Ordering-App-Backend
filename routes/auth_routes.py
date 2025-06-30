from flask import Blueprint, request, jsonify
from database import db
from models import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__)
ALLOWED_ORIGINS = ["http://localhost:3000", "https://styleflex-frontend.vercel.app"]

# ======================
# Register
# ======================
@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
def register():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 409

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ======================
# Login
# ======================
@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
def login():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            user={"id": user.id, "username": user.username, "email": user.email}
        ), 200

    return jsonify({"message": "Invalid credentials"}), 401

# ======================
# Refresh Token
# ======================
@auth_bp.route('/refresh', methods=['POST', 'OPTIONS'])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
@jwt_required(refresh=True)
def refresh():
    if request.method == "OPTIONS":
        return '', 200

    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify(access_token=new_access_token), 200

# ======================
# Get Profile
# ======================
@auth_bp.route('/profile', methods=['GET', 'OPTIONS'])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
@jwt_required()
def profile():
    if request.method == "OPTIONS":
        return '', 200

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

# ======================
# Update Profile
# ======================
@auth_bp.route('/profile', methods=['PUT', 'OPTIONS'])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
@jwt_required()
def update_profile():
    if request.method == "OPTIONS":
        return '', 200

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"message": "Username already taken"}), 409
        user.username = data['username']

    if 'email' in data:
        user.email = data['email']

    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200
