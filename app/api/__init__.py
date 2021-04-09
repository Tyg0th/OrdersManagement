from flask import Blueprint
from flask_restx import Api

api = Blueprint('api', __name__)
api_restx = Api(api)