from flask_restx import Api
from app.api import api_restx


orders_ns = api_restx.namespace("orders", description="Orders operations")

from . import routes
