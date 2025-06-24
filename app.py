from flask import Flask
print("✅ Imported Flask")

from flask_jwt_extended import JWTManager
print("✅ Imported JWTManager")

from flask_cors import CORS
print("✅ Imported CORS")

from flask_migrate import Migrate
print("✅ Imported Migrate")

from database import db
print("✅ Imported db")

from routes import auth_bp, designs_bp, orders_bp
print("✅ Imported auth_bp, designs_bp, and orders_bp")

from config.config import Config
print("✅ Imported Config")

from models import User 
print("✅ Imported User model")

app = Flask(__name__)
app.config.from_object(Config)
print("⚙️ Config loaded")

db.init_app(app)
print("✅ db.init_app(app) complete")

migrate = Migrate(app, db)
print("✅ Migrate initialized")

JWTManager(app)
print("✅ JWTManager initialized")

CORS(app)
print("✅ CORS initialized")

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(designs_bp, url_prefix="/api/designs")
app.register_blueprint(orders_bp, url_prefix="/api/orders")
print("✅ All Blueprints registered")

def create_app():
    return app

if __name__ == "__main__":
    print("🧪 Running app directly...")
    app.run(debug=True)
