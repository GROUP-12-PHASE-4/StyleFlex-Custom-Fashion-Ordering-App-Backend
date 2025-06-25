from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, Design, User
from database import db
from utils import admin_required
import json

order_bp = Blueprint("order_bp", __name__)

@order_bp.route("/orders", methods=["GET"])
@jwt_required()
def get_orders():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)

    if user.is_admin:
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=current_user_id).all()

    return jsonify([order.to_dict() for order in orders]), 200

@order_bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    new_order = Order(
        user_id=current_user_id,
        design_id=data["design_id"],
        size=data.get("size"),
        measurements=json.dumps(data.get("measurements")) if data.get("measurements") else None,
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@order_bp.route("/orders/<int:id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data.get("status", order.status)
    db.session.commit()
    return jsonify(order.to_dict()), 200

@order_bp.route("/orders/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 200

orders_bp = order_bp
