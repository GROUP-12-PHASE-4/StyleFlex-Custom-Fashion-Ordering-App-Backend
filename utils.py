from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from functools import wraps
from models import User

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        if not user.is_admin:
            return jsonify({"message": "Admin access required"}), 403

        return func(*args, **kwargs)
    
    return wrapper
