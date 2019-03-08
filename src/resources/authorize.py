"""
Define the REST verbs relative to the JWT tokens
"""

from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask.json import jsonify
from flask import make_response, abort
from repositories import ChannelRepository
from repositories import GitlabProvider
from util import parse_params
from util import ApiError
# from flask import current_app as app


from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


class AuthorizeResource(Resource):
    @staticmethod
    @swag_from('../swagger/authorize/POST.yml')
    @parse_params(
        Argument(
            'client_id',
            location='json',
            required=True,
            help='The client_id for this client'
        ),
        Argument(
            'client_secret',
            location='json',
            required=True,
            help='The client_secret for this channel'
        )
    )
    def post(client_id, client_secret):
        """ Return an channel key information based on his slug """
        return make_response(ApiError("Invalid credentials",
                                      {"error": "The credentials provided are invalid"}).get_response())
