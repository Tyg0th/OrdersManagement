from app.api import api_restx

products_ns = api_restx.namespace("products", description="Products operations")

from . import routes
