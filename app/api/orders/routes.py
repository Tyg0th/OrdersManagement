import json
from app import db
from flask import request, Response, jsonify
from flask_restx import Resource, fields, ValidationError, SchemaModel
from . import orders_ns
from app.api import api_restx as orders_api
from app.api.orders.models import (
    Orders,
    OrderStatus,
    OrderDetail,
    orders_detail_schema,
    order_detail_schema,
    order_status_schema,
    order_schema,
    orders_schema
)
from app.api.clients.models import Clients
from ..products.models import Products

product_order_model = orders_api.model('ProductMetadata', {
    'product_id': fields.Integer(required=True),
    'quantity': fields.Integer(required=True, min=1),
    'price': fields.Float(required=True, min=1),
})

model = orders_api.model('OrdersModel', {
    'client_id': fields.Integer(required=True),
    'products': fields.List(
        fields.Nested(product_order_model)
    ),
})

model_status = orders_api.model('OrderStatus', {
    'status': fields.String()
})


@orders_ns.route('/')
class OrderList(Resource):
    def get(self):
        query_orders = Orders.query.filter_by(db_status=True).all()
        response = []
        for order in query_orders:
            dump_order = order_schema.dump(order)
            dump_order["details"] = []
            query_details = OrderDetail.query.filter_by(order_id=order.id).all()
            dump_details = orders_detail_schema.dump(query_details)
            for dump_details in dump_details:
                dump_order["details"].append(dump_details)

            response.append(dump_order)
        return jsonify(response)

    @orders_api.expect(model)
    def post(self):
        request_data = request.get_json()
        try:
            result = order_detail_schema.load(request_data)
        except (ValidationError, TypeError) as err:
            print(err)
            return {"errors": err.messages}, 422
        client = Clients.query.filter_by(
            id=request_data['client_id'], db_status=True
        ).first_or_404(
            description="Client not found"
        )

        for product in request_data['products']:
            query_product = Products.query.filter_by(
                id=product['product_id'],
                db_status=True
            ).first_or_404(
                description="Product not found"
            )
        new_order = Orders(
            client=client.id
        )
        db.session.add(new_order)
        db.session.flush()

        for index, product in enumerate(request_data['products'], start=1):
            new_order_detail = OrderDetail(
                id=index,
                order_id=new_order.id,
                product_id=product["product_id"],
                quantity=product["quantity"],
                price=product["price"]
            )
            db.session.add(new_order_detail)
            db.session.commit()

        return Response(201)


@orders_api.doc(responses={404: "Product not found", 200: "Succesfully"})
@orders_ns.route('/<int:id>')
class Order(Resource):
    def get(self, id):
        query_order = Orders.query.filter_by(db_status=True, id=id).first_or_404()
        response = {'order': order_schema.dump(query_order), 'details': []}
        query_details = OrderDetail.query.filter_by(order_id=query_order.id).all()
        dump_details = orders_detail_schema.dump(query_details)
        for detail in dump_details:
            response['details'].append(detail)
        return jsonify(response)

    @orders_api.expect(model_status)
    def put(self, id):
        request_data = request.get_json()
        try:
            result = order_status_schema.load(request_data)
        except (ValidationError, TypeError) as err:
            return {"errors": err.messages}, 422
        query_order = Orders.query.filter_by(db_status=True, id=id).first_or_404()
        if request_data["status"] == "Solicitada":
            query_order.status = OrderStatus.REQUESTED
        elif request_data["status"] == "Aprobada":
            query_order.status = OrderStatus.APPROVED
        else:
            query_order.status = OrderStatus.CANCELED

        db.session.add(query_order)
        db.session.commit()
        return Response(200)

    def delete(self, id):
        query_order = Orders.query.filter_by(db_status=True, id=id).first_or_404()
        query_order.db_status = False
        db.session.add(query_order)
        db.session.commit()
        return Response(200)
