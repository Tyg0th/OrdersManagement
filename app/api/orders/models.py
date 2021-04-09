from app import db
from app.core.models import TimestampedModel


class Orders(TimestampedModel, db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)


class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)
