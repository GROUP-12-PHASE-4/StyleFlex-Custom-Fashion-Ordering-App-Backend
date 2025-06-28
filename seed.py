from app import create_app
from database import db
from models import User, Design, Order

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Tables reset")

    admin = User(username="admin", email="admin@example.com", is_admin=True)
    admin.set_password("admin123")


    user = User(username="john", email="john@example.com")
    user.set_password("password123")

    design1 = Design(
        title="Classic Suit",
        description="Elegant black suit for formal events.",
        image="https://via.placeholder.com/300",
        category="Suits"
    )

    design2 = Design(
        title="Summer Dress",
        description="Lightweight floral dress for summer.",
        image="https://via.placeholder.com/300",
        category="Dresses"
    )

    db.session.add_all([admin, user, design1, design2])
    db.session.commit()
    print("✅ Users and designs added")


    order1 = Order(
        user_id=user.id,
        design_id=design1.id,
        size="M",
        measurements='{"chest": 38, "waist": 32, "length": 40}',
        status="pending"
    )

    db.session.add(order1)
    db.session.commit()
    print("✅ Sample order added")
