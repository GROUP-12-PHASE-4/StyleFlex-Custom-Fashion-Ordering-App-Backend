from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from models import Order, Design, User
from database import db
from utils import admin_required
import json

order_bp = Blueprint("order_bp", __name__)
ALLOWED_ORIGINS = ["http://localhost:3000", "https://styleflex-frontend.vercel.app"]

# ==========================
# /api/orders (GET, POST, OPTIONS)
# ==========================
@order_bp.route("/", methods=["OPTIONS", "GET", "POST"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
@jwt_required(optional=True)
def orders_handler():
    if request.method == "OPTIONS":
        return '', 200

    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"message": "Unauthorized"}), 401

    if request.method == "GET":
        user = User.query.get_or_404(current_user_id)
        orders = Order.query.all() if user.is_admin else Order.query.filter_by(user_id=current_user_id).all()
        return jsonify([order.to_dict() for order in orders]), 200

    if request.method == "POST":
        data = request.get_json()
        new_order = Order(
            user_id=current_user_id,
            design_id=data["design_id"],
            size=data.get("size"),
            measurements=json.dumps(data.get("measurements")) if data.get("measurements") else None,
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify(new_order.to_dict()), 201

# ==========================
# /api/orders/<id> (PUT, DELETE, OPTIONS)
# ==========================
@order_bp.route("/<int:id>", methods=["OPTIONS", "PUT", "DELETE"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
@jwt_required()
@admin_required
def order_admin_actions(id):
    if request.method == "OPTIONS":
        return '', 200

    order = Order.query.get_or_404(id)

    if request.method == "PUT":
        data = request.get_json()
        order.status = data.get("status", order.status)
        db.session.commit()
        return jsonify(order.to_dict()), 200

    if request.method == "DELETE":
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted"}), 200

# ==========================
# /api/orders/<id>/offer (POST, OPTIONS)
# ==========================
@order_bp.route("/<int:id>/offer", methods=["OPTIONS", "POST"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
@jwt_required()
def make_offer(id):
    if request.method == "OPTIONS":
        return '', 200

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
