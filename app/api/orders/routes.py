from flask_restx import Resource
from . import orders_ns
from app.api import api_restx as orders_api


@orders_ns.route('/hello_orders')
@orders_api.doc(responses={404: "Todo not found"}, params={"todo_id": "The Todo ID"})
class HelloWorldOrders(Resource):
    def get(self):
        return {"msg": "hola"}