from flask import Flask, request
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

# ✅ Apply CORS to the app
CORS(
    app,
    resources={r"/api/*": {"origins": [
        "http://localhost:3000",
        "https://styleflex-frontend.vercel.app"
    ]}},
    supports_credentials=True
)
print("✅ CORS initialized")

# ✅ Global CORS headers for all responses
@app.after_request
def apply_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin in ["http://localhost:3000", "https://styleflex-frontend.vercel.app"]:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# ✅ Preflight support to avoid 405s
@app.route('/api/<path:path>', methods=["OPTIONS"])
def handle_options(path):
    return '', 200

# ✅ Initialize database and extensions
db.init_app(app)
migrate = Migrate(app, db)
JWTManager(app)

# ✅ Register blueprints with correct prefixes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(designs_bp, url_prefix="/api/designs")
app.register_blueprint(orders_bp, url_prefix="/api/orders")

@app.route("/")
def index():
    return {"message": "StyleFlex API is running 🚀"}, 200

def create_app():
    return app

if __name__ == "__main__":
    print("🧪 Running in development mode")
    app.run(debug=True)
