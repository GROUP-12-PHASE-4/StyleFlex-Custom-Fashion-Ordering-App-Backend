from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Design
from database import db
from utils import admin_required

designs_bp = Blueprint("designs_bp", __name__)


@designs_bp.route("/", methods=["GET"])
def get_designs():
    designs = Design.query.all()
    return jsonify([design.to_dict() for design in designs]), 200


@designs_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_design():
    data = request.get_json()
    new_design = Design(
        title=data.get("title"),
        description=data.get("description"),
        image=data.get("image"),
        category=data.get("category")
    )
    db.session.add(new_design)
    db.session.commit()
    return jsonify(new_design.to_dict()), 201

@designs_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_design(id):
    design = Design.query.get_or_404(id)
    data = request.get_json()
    design.title = data.get("title", design.title)
    design.description = data.get("description", design.description)
    design.image = data.get("image", design.image)
    design.category = data.get("category", design.category)
    db.session.commit()
    return jsonify(design.to_dict()), 200

@designs_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_design(id):
    design = Design.query.get_or_404(id)
    db.session.delete(design)
    db.session.commit()
    return jsonify({"message": "Design deleted"}), 200
