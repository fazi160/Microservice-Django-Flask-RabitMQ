# currently no use

from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)


class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='user_product_unique'),
    )
