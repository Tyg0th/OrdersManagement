from app import db, ma
from app.core.models import TimestampedModel


class Products(TimestampedModel, db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, nullable=True)


class ProductsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Products

    name = ma.auto_field()
    price = ma.auto_field()
    stock = ma.auto_field()


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
