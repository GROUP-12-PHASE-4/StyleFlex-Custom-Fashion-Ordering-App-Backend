from app import app
from database import db
from models import User

def seed_admin():
    with app.app_context():
       
        admin = User.query.filter_by(email="admin@example.com").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                is_admin=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")
        else:
            print("⚠️ Admin already exists")

if __name__ == "__main__":
    seed_admin()
