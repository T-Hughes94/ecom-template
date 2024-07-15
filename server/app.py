#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, session
from flask_restful import Resource
from models import User, Product

# Local imports
from config import app, db, api
# Add your model imports

@app.route('/')
def index():
    return '<h1>E-commerce Project Server</h1>'

class UserRoute(Resource):
    def get(self):
        users = [u.to_dict() for u in User.query.all()]
        return users, 200

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        new_user.password_hash = data['password']
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return new_user.to_dict(), 201

api.add_resource(UserRoute, '/users')

class ProductRoute(Resource):
    def get(self):
        products = [p.to_dict() for p in Product.query.all()]
        return products, 200

    def post(self):
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock']
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict(), 201

api.add_resource(ProductRoute, '/products')