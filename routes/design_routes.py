from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from models import Design
from database import db
from utils import admin_required

designs_bp = Blueprint("designs_bp", __name__)
ALLOWED_ORIGINS = ["http://localhost:3000", "https://styleflex-frontend.vercel.app"]

# ========== GET All Designs ==========
@designs_bp.route("/", methods=["GET"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
def get_designs():
    designs = Design.query.all()
    return jsonify([design.to_dict() for design in designs]), 200

# ========== OPTIONS Preflight for POST ==========
@designs_bp.route("/", methods=["OPTIONS"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
def designs_options():
    return '', 200

# ========== POST New Design ==========
@designs_bp.route("/", methods=["POST"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
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

# ========== OPTIONS for PUT ==========
@designs_bp.route("/<int:id>", methods=["OPTIONS"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
def design_put_options(id):
    return '', 200

# ========== PUT Update Design ==========
@designs_bp.route("/<int:id>", methods=["PUT"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
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

# ========== OPTIONS for DELETE ==========
@designs_bp.route("/<int:id>", methods=["OPTIONS"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
def design_delete_options(id):
    return '', 200

# ========== DELETE Design ==========
@designs_bp.route("/<int:id>", methods=["DELETE"])
@cross_origin(origins=ALLOWED_ORIGINS, supports_credentials=True)
@jwt_required()
@admin_required
def delete_design(id):
    design = Design.query.get_or_404(id)
    db.session.delete(design)
    db.session.commit()
    return jsonify({"message": "Design deleted"}), 200
