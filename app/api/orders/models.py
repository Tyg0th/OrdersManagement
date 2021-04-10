import enum
from app import db, ma
from app.core.models import TimestampedModel, IsDeleted
from app.api.products.models import Products
from sqlalchemy import UniqueConstraint
from flask_marshmallow.fields import fields
from marshmallow import validate


class OrderStatus(enum.Enum):
    REQUESTED = "Solicitada"
    APPROVED = "Aprobada"
    CANCELED = "Cancelada"


class Orders(IsDeleted, TimestampedModel, db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.Integer, db.ForeignKey('clients.id'))
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.REQUESTED)


class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, unique=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)


class ProductsMetadata(ma.SQLAlchemySchema):
    class Meta:
        model = Products
    product_id = fields.Integer()
    quantity = fields.Integer()
    price = fields.Float()


class OrdersDetailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OrderDetail
    client_id = fields.Integer()
    products = fields.List(fields.Nested(ProductsMetadata))


class OrdersDetailSchemaGet(ma.SQLAlchemySchema):
    class Meta:
        model = OrderDetail
        fields = ('product_id', 'quantity', 'price')
    client_id = fields.Integer()
    products = fields.List(fields.Nested(ProductsMetadata))


class OrdersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OrderDetail
        model = Orders
        fields = ['id', 'client', 'status', 'products']

    status = fields.Function(lambda x: x.status.value)
    products = fields.Nested(OrdersDetailSchema)


class OrderStatusSchema(ma.Schema):
    status = fields.Str(validate=validate.OneOf(["Solicitada", "Aprobada", "Cancelada"]))


order_status_schema = OrderStatusSchema()
order_detail_schema = OrdersDetailSchema()
orders_detail_schema = OrdersDetailSchema(many=True)

orders_detail_get_schema = OrdersDetailSchemaGet(many=True)

order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)