"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api
from util import API_ERRORS
from resources import AuthorizeResource


AUTHORIZE_BLUEPRINT = Blueprint('authorize', __name__)
Api(AUTHORIZE_BLUEPRINT, catch_all_404s=True, errors=API_ERRORS).add_resource(
    AuthorizeResource,
    '/authorize'
)
