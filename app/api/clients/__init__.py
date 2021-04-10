from app.api import api_restx

clients_ns = api_restx.namespace("clients", description="clients operations")

from . import routes
