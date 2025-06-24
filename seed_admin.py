from app import app
from database import db
from models import User

with app.app_context():
    username = "adminuser"
    email = "admin@example.com"
    password = "adminpassword"

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        print(f"ℹ️ A user with username '{username}' or email '{email}' already exists.")
    else:
        admin = User(username=username, email=email, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Admin user '{username}' created successfully.")
