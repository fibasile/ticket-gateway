"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api
from util import API_ERRORS
from resources import ClientResource


CLIENT_BLUEPRINT = Blueprint('client', __name__)
Api(CLIENT_BLUEPRINT, catch_all_404s=True, errors=API_ERRORS).add_resource(
    ClientResource,
    '/client/<string:slug>'
)
