from flask import jsonify, request, Response
from flask_restx import Resource, fields, ValidationError
from marshmallow import ValidationError

from app import db
from . import clients_ns
from app.api import api_restx as clients_api
from app.api.clients.models import Clients, clients_schema, client_schema

model = clients_api.model('ClientsModel', {
    'name': fields.String(required=True),
    'address': fields.String(required=True),
    'phone_number': fields.String(required=True),
    'citizenship': fields.String(required=True),
    'email': fields.String(required=True)
})


@clients_ns.route('/')
class ClientList(Resource):
    def get(self):
        all_clients = Clients.query.filter_by(db_status=True).all()
        return clients_schema.dump(all_clients)

    @clients_api.doc(responses={201: "Client created"})
    @clients_api.expect(model)
    def post(self):
        request_data = request.get_json()
        try:
            result = client_schema.load(request_data)
        except (ValidationError, TypeError) as err:
            print(err)
            return {"errors": err.messages}, 422
        new_client = Clients(
            name= request_data["name"],
            address=request_data["address"],
            phone_number=request_data["phone_number"],
            citizenship=request_data["citizenship"],
            email=request_data["email"],
        )
        db.session.add(new_client)
        db.session.commit()
        return Response(status=201)


@clients_api.doc(responses={404: "Product not found", 200: "Succesfully"})
@clients_ns.route('/<int:id>')
class Client(Resource):
    def get(self, id):
        query_client = Clients.query.filter_by(db_status=True, id=id).first_or_404()
        return client_schema.dump(query_client)

    @clients_api.expect(model)
    def put(self, id):
        request_data = request.get_json()
        try:
            result = client_schema.load(request_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        query_client = Clients.query.filter_by(db_status=True, id=id).first_or_404()
        query_client.name = request_data["name"]
        query_client.address = request_data["address"]
        query_client.phone_number = request_data["phone_number"]
        query_client.email = request_data["email"]
        db.session.add(query_client)
        db.session.comit()
        return Response(200)

    def delete(selfself, id):
        query_client = Clients.query.filter_by(db_status=True, id=id).first_or_404()
        query_client.db_status = False
        db.session.add(query_client)
        db.session.commit()
        return Response(200)
