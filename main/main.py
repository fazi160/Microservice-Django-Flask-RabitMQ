from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from producer import publish
# 1:08:15

db = SQLAlchemy()

app = Flask(__name__)

# Database configuration directly from hardcoded values
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:root@db:5432/main"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db object with the app
db.init_app(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)


class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id',
                            name='user_product_unique'),
    )


@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Fetch all products from the database.
    """
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'title': product.title,
        'image': product.image
    } for product in products])




@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/user')
    json = req.json()

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success'
    })



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created before starting the server
    app.run(debug=True, host='0.0.0.0', port=5000)
