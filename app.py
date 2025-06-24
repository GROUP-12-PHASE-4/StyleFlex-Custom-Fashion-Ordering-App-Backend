print("📦 app.py has started importing...")

from flask import Flask
print("✅ Imported Flask")

from flask_jwt_extended import JWTManager
print("✅ Imported JWTManager")

from flask_cors import CORS
print("✅ Imported CORS")

from database import db
print("✅ Imported db")

from routes import auth_bp
print("✅ Imported auth_bp")

from config.config import Configonfig
print("✅ Imported Config")


def create_app():
    print("🚀 create_app is starting...")
    app = Flask(__name__)
    app.config.from_object(Config)
    print("⚙️ Config loaded")

    db.init_app(app)
    print("✅ db.init_app(app) complete")

    JWTManager(app)
    print("✅ JWTManager initialized")

    CORS(app)
    print("✅ CORS initialized")

    app.register_blueprint(auth_bp, url_prefix="/api")
    print("✅ Blueprint registered")

    return app


if __name__ == "__main__":
    print("🧪 Running app directly...")
    app = create_app()
    print("✅ App created")
    app.run(debug=True)
