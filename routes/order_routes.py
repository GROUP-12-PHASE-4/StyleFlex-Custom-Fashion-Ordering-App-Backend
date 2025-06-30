from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from models import Order, Design, User
from database import db
from utils import admin_required
import json

order_bp = Blueprint("order_bp", __name__)

# Handle CORS preflight requests (OPTIONS) for /orders
@order_bp.route("/orders", methods=["OPTIONS"])
@cross_origin()
def orders_options():
    return '', 200

# GET /orders - fetch orders
@order_bp.route("/orders", methods=["GET"])
@jwt_required()
@cross_origin()
def get_orders():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)

    if user.is_admin:
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=current_user_id).all()

    return jsonify([order.to_dict() for order in orders]), 200

# Handle OPTIONS preflight for POST
@order_bp.route("/orders", methods=["OPTIONS"])
@cross_origin()
def create_order_options():
    return '', 200

# POST /orders - create new order
@order_bp.route("/orders", methods=["POST"])
@jwt_required()
@cross_origin()
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

# OPTIONS for PUT
@order_bp.route("/orders/<int:id>", methods=["OPTIONS"])
@cross_origin()
def update_order_options(id):
    return '', 200

# PUT /orders/<id> - update order status
@order_bp.route("/orders/<int:id>", methods=["PUT"])
@jwt_required()
@admin_required
@cross_origin()
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data.get("status", order.status)
    db.session.commit()
    return jsonify(order.to_dict()), 200

# OPTIONS for DELETE
@order_bp.route("/orders/<int:id>", methods=["OPTIONS"])
@cross_origin()
def delete_order_options(id):
    return '', 200

# DELETE /orders/<id> - delete order
@order_bp.route("/orders/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
@cross_origin()
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 200

# OPTIONS for /offer
@order_bp.route("/orders/<int:id>/offer", methods=["OPTIONS"])
@cross_origin()
def offer_options(id):
    return '', 200

# POST /orders/<id>/offer - tailor makes offer
@order_bp.route("/orders/<int:id>/offer", methods=["POST"])
@jwt_required()
@cross_origin()
def make_offer(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    offer_price = data.get("offer_price")
    notes = data.get("notes")

    if not offer_price:
        return jsonify({"message": "Offer price is required"}), 400

    offer_data = {
        "offer_price": offer_price,
        "notes": notes,
        "tailor_id": get_jwt_identity(),
    }

    order.offer = json.dumps(offer_data)
    db.session.commit()

    return jsonify({"message": "Offer made successfully", "offer": offer_data}), 200

# Export blueprint
orders_bp = order_bp
