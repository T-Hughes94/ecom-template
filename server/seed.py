# seed.py
from app import app
from models import db, User, Product

if __name__ == '__main__':

    with app.app_context():
        db.drop_all()
        db.create_all()

        user1 = User(username="Alice", email="alice@example.com")
        user1.password_hash = "password1"
        user2 = User(username="Bob", email="bob@example.com")
        user2.password_hash = "password2"

        product1 = Product(name="Laptop", description="A powerful laptop", price=999.99, stock=10)
        product2 = Product(name="Smartphone", description="A modern smartphone", price=699.99, stock=15)

        db.session.add_all([user1, user2, product1, product2])
        db.session.commit()

