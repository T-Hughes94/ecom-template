# seed.py
from app import app
from models import db, User, Category, Product, Order, OrderItem, Cart, CartItem

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create Users
        user1 = User(username="Alice", email="alice@example.com", password="password1")
        user2 = User(username="Bob", email="bob@example.com", password="password2")

        db.session.add_all([user1, user2])
        db.session.commit()

        # Create Categories
        category1 = Category(name="Electronics")
        category2 = Category(name="Clothing")

        db.session.add_all([category1, category2])
        db.session.commit()

        # Create Products
        product1 = Product(name="Laptop", description="A powerful laptop", price=999.99, stock=10, category_id=category1.id)
        product2 = Product(name="Smartphone", description="A modern smartphone", price=699.99, stock=15, category_id=category1.id)
        product3 = Product(name="T-Shirt", description="A comfortable cotton t-shirt", price=19.99, stock=50, category_id=category2.id)

        db.session.add_all([product1, product2, product3])
        db.session.commit()

        # Create Orders
        order1 = Order(user_id=user1.id, total_amount=1699.98, status="Completed")
        order2 = Order(user_id=user2.id, total_amount=19.99, status="Processing")

        db.session.add_all([order1, order2])
        db.session.commit()

        # Create OrderItems
        order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1, price=999.99)
        order_item2 = OrderItem(order_id=order1.id, product_id=product2.id, quantity=1, price=699.99)
        order_item3 = OrderItem(order_id=order2.id, product_id=product3.id, quantity=1, price=19.99)

        db.session.add_all([order_item1, order_item2, order_item3])
        db.session.commit()

        # Create Carts
        cart1 = Cart(user_id=user1.id)
        cart2 = Cart(user_id=user2.id)

        db.session.add_all([cart1, cart2])
        db.session.commit()

        # Create CartItems
        cart_item1 = CartItem(cart_id=cart1.id, product_id=product3.id, quantity=2)
        cart_item2 = CartItem(cart_id=cart2.id, product_id=product1.id, quantity=1)

        db.session.add_all([cart_item1, cart_item2])
        db.session.commit()

        print("Seed completed.")


