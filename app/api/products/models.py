from app import db, ma
from app.core.models import TimestampedModel, IsDeleted


class Products(IsDeleted, TimestampedModel, db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)


class ProductsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Products

    name = ma.auto_field()
    price = ma.auto_field()
    stock = ma.auto_field()
    width = ma.auto_field()
    height = ma.auto_field()


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
