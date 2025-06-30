from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

from database import db
from routes import auth_bp, designs_bp, orders_bp
from config.config import Config
from models import User, Design, Order

print("✅ All modules imported")

app = Flask(__name__)
app.config.from_object(Config)
print("⚙️ Config loaded")

# ✅ Apply CORS immediately
CORS(
    app,
    resources={r"/api/*": {"origins": [
        "http://localhost:3000",
        "https://styleflex-frontend.vercel.app"
    ]}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)
print("✅ CORS initialized")

db.init_app(app)
print("✅ Database initialized")

migrate = Migrate(app, db)
print("✅ Migrations setup")

JWTManager(app)
print("✅ JWT Manager setup")

# ✅ Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(designs_bp, url_prefix="/api/designs")
app.register_blueprint(orders_bp, url_prefix="/api/orders")
print("✅ Blueprints registered")

@app.route("/")
def index():
    return {"message": "StyleFlex API is running 🚀"}, 200

def create_app():
    return app

if __name__ == "__main__":
    print("🧪 Running in development mode")
    app.run(debug=True)
