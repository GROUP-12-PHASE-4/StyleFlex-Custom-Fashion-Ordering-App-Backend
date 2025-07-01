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

# ✅ Allow both trailing and non-trailing slashes in routes
app.url_map.strict_slashes = False

print("⚙️ Config loaded")

# ✅ Apply CORS to the app
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

# ✅ Apply global CORS headers for all responses
@app.after_request
def apply_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin in ["http://localhost:3000", "https://styleflex-frontend.vercel.app"]:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# ✅ Handle OPTIONS preflight requests explicitly
@app.route('/api/<path:path>', methods=["OPTIONS"])
def handle_options(path):
    return '', 200

# ✅ Initialize DB
db.init_app(app)
print("✅ Database initialized")

# ✅ Set up Migrations
migrate = Migrate(app, db)
print("✅ Migrations setup")

# ✅ JWT Setup
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
