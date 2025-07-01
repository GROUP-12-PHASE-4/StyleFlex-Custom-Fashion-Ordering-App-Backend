from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    orders = db.relationship("Order", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Design(db.Model):
    __tablename__ = "designs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String)
    category = db.Column(db.String(50))

    orders = db.relationship("Order", backref="design", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "category": self.category
        }

    def __repr__(self):
        return f"<Design {self.title}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    design_id = db.Column(db.Integer, db.ForeignKey("designs.id"), nullable=False)
    size = db.Column(db.String(20))
    measurements = db.Column(db.Text)  # Stored as JSON string
    status = db.Column(db.String(20), default="pending")
    offer = db.Column(db.Text)  # Stored as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "design_id": self.design_id,
            "size": self.size,
            "measurements": self._safe_json(self.measurements),
            "status": self.status,
            "offer": self._safe_json(self.offer),
            "created_at": self.created_at.isoformat(),
            "design": self.design.to_dict() if self.design else None
        }

    def _safe_json(self, field):
        try:
            return json.loads(field) if field else None
        except (ValueError, TypeError):
            return None

    def __repr__(self):
        return f"<Order {self.id} - User {self.user_id}>"
