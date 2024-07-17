# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy.ext.hybrid import hybrid_property


# from config import db, bcrypt

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False)
#     _password_hash = db.Column(db.String)
#     email = db.Column(db.String, nullable=False, unique=True)
    
#     @hybrid_property
#     def password_hash(self):
#         return self._password_hash

#     @password_hash.setter
#     def password_hash(self, password):
#         self._password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

#     def authenticate(self, password):
#         return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

#     @validates('username', 'email')
#     def validate_fields(self, key, value):
#         if key == 'username':
#             if not isinstance(value, str) or len(value) < 1:
#                 raise ValueError('Username must be a non-empty string')
#         if key == 'email':
#             if not isinstance(value, str) or '@' not in value:
#                 raise ValueError('Email must be a valid email address')
#         return value

#     class Product(db.Model, SerializerMixin):
#         __tablename__ = 'products'
#         id = db.Column(db.Integer, primary_key=True)
#         name = db.Column(db.String(255), nullable=False)
#         description = db.Column(db.String, nullable=False)
#         price = db.Column(db.Float, nullable=False)
#         stock = db.Column(db.Integer, default=0)

#     @validates('name')
#     def validate_name(self, key, name):
#         if not name or not isinstance(name, str) or len(name) > 255:
#             raise ValueError('Name must be a non-empty string with a maximum length of 255 characters')
#         return name

#     @validates('description')
#     def validate_description(self, key, description):
#         if not description or not isinstance(description, str):
#             raise ValueError('Description must be a non-empty string')
#         return description

#     @validates('price')
#     def validate_price(self, key, price):
#         if price is None or not isinstance(price, (int, float)) or price < 0:
#             raise ValueError('Price must be a non-negative number')
#         return price

#     @validates('stock')
#     def validate_stock(self, key, stock):
#         if stock is None or not isinstance(stock, int) or stock < 0:
#             raise ValueError('Stock must be a non-negative integer')
#         return stock


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', back_populates='user')
    carts = db.relationship('Cart', back_populates='user')

    serialize_only = ('id', 'username', 'email', 'created_at')

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password.encode('utf-8'))

    @validates('username', 'email')
    def validate_fields(self, key, value):
        if key == 'username':
            if not isinstance(value, str) or len(value) < 1:
                raise ValueError('Username must be a non-empty string')
        if key == 'email':
            if not isinstance(value, str) or '@' not in value:
                raise ValueError('Email must be a valid email address')
        return value


class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    products = db.relationship('Product', back_populates='category')

    serialize_only = ('id', 'name')


class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category = db.relationship('Category', back_populates='products')
    order_items = db.relationship('OrderItem', back_populates='product')
    cart_items = db.relationship('CartItem', back_populates='product')

    serialize_only = ('id', 'name', 'description', 'price', 'stock', 'category_id', 'created_at')

    @validates('name', 'description', 'price', 'stock')
    def validate_fields(self, key, value):
        if key == 'name' and (not value or not isinstance(value, str) or len(value) > 255):
            raise ValueError('Name must be a non-empty string with a maximum length of 255 characters')
        if key == 'description' and (not value or not isinstance(value, str)):
            raise ValueError('Description must be a non-empty string')
        if key == 'price' and (value is None or not isinstance(value, (int, float)) or value < 0):
            raise ValueError('Price must be a non-negative number')
        if key == 'stock' and (value is None or not isinstance(value, int) or value < 0):
            raise ValueError('Stock must be a non-negative integer')
        return value


class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order')

    serialize_only = ('id', 'user_id', 'total_amount', 'status', 'created_at')

    @validates('total_amount', 'status')
    def validate_fields(self, key, value):
        if key == 'total_amount' and (value is None or not isinstance(value, (int, float)) or value < 0):
            raise ValueError('Total amount must be a non-negative number')
        if key == 'status' and (not value or not isinstance(value, str)):
            raise ValueError('Status must be a non-empty string')
        return value


class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='order_items')

    serialize_only = ('id', 'order_id', 'product_id', 'quantity', 'price')

    @validates('quantity', 'price')
    def validate_fields(self, key, value):
        if key == 'quantity' and (value is None or not isinstance(value, int) or value < 0):
            raise ValueError('Quantity must be a non-negative integer')
        if key == 'price' and (value is None or not isinstance(value, (int, float)) or value < 0):
            raise ValueError('Price must be a non-negative number')
        return value


class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='carts')
    cart_items = db.relationship('CartItem', back_populates='cart')

    serialize_only = ('id', 'user_id', 'created_at')


class CartItem(db.Model, SerializerMixin):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    cart = db.relationship('Cart', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')

    serialize_only = ('id', 'cart_id', 'product_id', 'quantity')

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity is None or not isinstance(quantity, int) or quantity < 0:
            raise ValueError('Quantity must be a non-negative integer')
        return quantity

