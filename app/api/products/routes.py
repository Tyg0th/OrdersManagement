from flask_restx import Resource, fields, ValidationError
from flask import request, jsonify, Response

from app import db
from . import products_ns
from app.api import api_restx as products_api
from app.api.products.models import Products, product_schema, products_schema

model = products_api.model('ProductsModel', {
    'name': fields.String(required=True),
    'price': fields.Float(min=1),
    'stock': fields.Integer(min=1),
    'width': fields.Float(),
    'height': fields.Float(),
})


@products_ns.route('/')
class ProductList(Resource):
    @products_api.doc(responses={404: "Product not found", 200: "Succesfully"})
    def get(self):
        all_products = Products.query.filter_by(db_status=True).all()
        return products_schema.dump(all_products)

    @products_api.doc(responses={201: "Created"})
    @products_api.expect(model)
    def post(self):
        request_data = request.get_json()
        try:
            result = product_schema.load(request_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        new_product = Products(
            name=request_data["name"],
            price=request_data["price"],
            stock=request_data["stock"],
            width=request_data["width"],
            height=request_data["height"],
        )
        db.session.add(new_product)
        db.session.commit()
        return Response(status=201)


@products_api.doc(responses={404: "Product not found", 200: "Succesfully"})
@products_ns.route('/<int:id>')
class Product(Resource):
    def get(self, id):
        query_product = Products.query.filter_by(db_status=True, id=id).first_or_404()
        return product_schema.dump(query_product)

    @products_api.expect(model)
    def put(self, id):
        request_data = request.get_json()
        try:
            result = product_schema.load(request_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        query_product = Products.query.filter_by(db_status=True, id=id).first_or_404()
        query_product.name = request_data["name"]
        query_product.price = request_data["price"]
        query_product.stock = request_data["stock"]
        db.session.add(query_product)
        db.session.commit()
        return Response(200)

    def delete(selfself, id):
        query_product = Products.query.filter_by(db_status=True, id=id).first_or_404()
        query_product.db_status = False
        db.session.add(query_product)
        db.session.commit()
        return Response(200)


