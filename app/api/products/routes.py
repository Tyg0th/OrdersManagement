from flask_restx import Resource
from . import products_ns
from app.api import api_restx as products_api
from app.api.products.models import Products, product_schema, products_schema


@products_ns.route('/')
@products_api.doc(responses={404: "Todo not found"}, params={"products_id": "The Todo ID"})
class ProductsResource(Resource):
    def get(self):
        all_products = Products.query.all()
        return products_schema.dump(all_products)
