from app import app
from database import db
from models import User

def seed_admin():
    with app.app_context():
        if User.query.filter_by(username="admin").first():
            print("⚠️ Admin user already exists.")
            return

        admin = User(
            username="admin",
            email="admin@example.com",
            is_admin=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created.")

if __name__ == "__main__":
    seed_admin()
