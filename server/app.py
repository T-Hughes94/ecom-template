from flask import request, session
from flask_restful import Resource
from models import User, Product, Category, Order, OrderItem, Cart, CartItem

# Local imports
from config import app, db, api

@app.route('/')
def index():
    return '<h1>E-commerce Project Server</h1>'

############################ User Routes ########################################
class UserRoute(Resource):
    def get(self):
        users = [u.to_dict() for u in User.query.all()]
        return users, 200
    
    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        new_user.password = data['password']
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return new_user.to_dict(), 201

api.add_resource(UserRoute, '/users')

class UserByIdRoute(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            return user.to_dict(), 200
        return {"error": "User not found"}, 404
    
    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user.to_dict(), 200
        return {"error": "User not found"}, 404
    
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return '', 204
        return {"error": "User not found"}, 404

api.add_resource(UserByIdRoute, '/users/<int:id>')

############################ Product Routes ########################################
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
            stock=data['stock'],
            category_id=data['category_id']
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict(), 201

api.add_resource(ProductRoute, '/products')

class ProductByIdRoute(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            return product.to_dict(), 200
        return {"error": "Product not found"}, 404
    
    def patch(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            data = request.get_json()
            for key, value in data.items():
                setattr(product, key, value)
            db.session.commit()
            return product.to_dict(), 200
        return {"error": "Product not found"}, 404
    
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return '', 204
        return {"error": "Product not found"}, 404

api.add_resource(ProductByIdRoute, '/products/<int:id>')

############################ Category Routes ########################################
class CategoryRoute(Resource):
    def get(self):
        categories = [c.to_dict() for c in Category.query.all()]
        return categories, 200
    
    def post(self):
        data = request.get_json()
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return new_category.to_dict(), 201

api.add_resource(CategoryRoute, '/categories')

class CategoryByIdRoute(Resource):
    def get(self, id):
        category = Category.query.filter_by(id=id).first()
        if category:
            return category.to_dict(), 200
        return {"error": "Category not found"}, 404
    
    def patch(self, id):
        category = Category.query.filter_by(id=id).first()
        if category:
            data = request.get_json()
            for key, value in data.items():
                setattr(category, key, value)
            db.session.commit()
            return category.to_dict(), 200
        return {"error": "Category not found"}, 404
    
    def delete(self, id):
        category = Category.query.filter_by(id=id).first()
        if category:
            db.session.delete(category)
            db.session.commit()
            return '', 204
        return {"error": "Category not found"}, 404

api.add_resource(CategoryByIdRoute, '/categories/<int:id>')

############################ Order Routes ########################################
class OrderRoute(Resource):
    def get(self):
        orders = [o.to_dict() for o in Order.query.all()]
        return orders, 200
    
    def post(self):
        data = request.get_json()
        new_order = Order(
            user_id=data['user_id'],
            total_amount=data['total_amount'],
            status=data['status']
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order.to_dict(), 201

api.add_resource(OrderRoute, '/orders')

class OrderByIdRoute(Resource):
    def get(self, id):
        order = Order.query.filter_by(id=id).first()
        if order:
            return order.to_dict(), 200
        return {"error": "Order not found"}, 404
    
    def patch(self, id):
        order = Order.query.filter_by(id=id).first()
        if order:
            data = request.get_json()
            for key, value in data.items():
                setattr(order, key, value)
            db.session.commit()
            return order.to_dict(), 200
        return {"error": "Order not found"}, 404
    
    def delete(self, id):
        order = Order.query.filter_by(id=id).first()
        if order:
            db.session.delete(order)
            db.session.commit()
            return '', 204
        return {"error": "Order not found"}, 404

api.add_resource(OrderByIdRoute, '/orders/<int:id>')

############################ OrderItem Routes ########################################
class OrderItemRoute(Resource):
    def get(self):
        order_items = [oi.to_dict() for oi in OrderItem.query.all()]
        return order_items, 200
    
    def post(self):
        data = request.get_json()
        new_order_item = OrderItem(
            order_id=data['order_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            price=data['price']
        )
        db.session.add(new_order_item)
        db.session.commit()
        return new_order_item.to_dict(), 201

api.add_resource(OrderItemRoute, '/order_items')

class OrderItemByIdRoute(Resource):
    def get(self, id):
        order_item = OrderItem.query.filter_by(id=id).first()
        if order_item:
            return order_item.to_dict(), 200
        return {"error": "OrderItem not found"}, 404
    
    def patch(self, id):
        order_item = OrderItem.query.filter_by(id=id).first()
        if order_item:
            data = request.get_json()
            for key, value in data.items():
                setattr(order_item, key, value)
            db.session.commit()
            return order_item.to_dict(), 200
        return {"error": "OrderItem not found"}, 404
    
    def delete(self, id):
        order_item = OrderItem.query.filter_by(id=id).first()
        if order_item:
            db.session.delete(order_item)
            db.session.commit()
            return '', 204
        return {"error": "OrderItem not found"}, 404

api.add_resource(OrderItemByIdRoute, '/order_items/<int:id>')

############################ Cart Routes ########################################
class CartRoute(Resource):
    def get(self):
        carts = [c.to_dict() for c in Cart.query.all()]
        return carts, 200
    
    def post(self):
        data = request.get_json()
        new_cart = Cart(user_id=data['user_id'])
        db.session.add(new_cart)
        db.session.commit()
        return new_cart.to_dict(), 201

api.add_resource(CartRoute, '/carts')

class CartByIdRoute(Resource):
    def get(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if cart:
            return cart.to_dict(), 200
        return {"error": "Cart not found"}, 404
    
    def patch(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if cart:
            data = request.get_json()
            for key, value in data.items():
                setattr(cart, key, value)
            db.session.commit()
            return cart.to_dict(), 200
        return {"error": "Cart not found"}, 404
    
    def delete(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if cart:
            db.session.delete(cart)
            db.session.commit()
            return '', 204
        return {"error": "Cart not found"}, 404

api.add_resource(CartByIdRoute, '/carts/<int:id>')

############################ CartItem Routes ########################################
class CartItemRoute(Resource):
    def get(self):
        cart_items = [ci.to_dict() for ci in CartItem.query.all()]
        return cart_items, 200
    
    def post(self):
        data = request.get_json()
        new_cart_item = CartItem(
            cart_id=data['cart_id'],
            product_id=data['product_id'],
            quantity=data['quantity']
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return new_cart_item.to_dict(), 201

api.add_resource(CartItemRoute, '/cart_items')

class CartItemByIdRoute(Resource):
    def get(self, id):
        cart_item = CartItem.query.filter_by(id=id).first()
        if cart_item:
            return cart_item.to_dict(), 200
        return {"error": "CartItem not found"}, 404
    
    def patch(self, id):
        cart_item = CartItem.query.filter_by(id=id).first()
        if cart_item:
            data = request.get_json()
            for key, value in data.items():
                setattr(cart_item, key, value)
            db.session.commit()
            return cart_item.to_dict(), 200
        return {"error": "CartItem not found"}, 404
    
    def delete(self, id):
        cart_item = CartItem.query.filter_by(id=id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return '', 204
        return {"error": "CartItem not found"}, 404

api.add_resource(CartItemByIdRoute, '/cart_items/<int:id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
