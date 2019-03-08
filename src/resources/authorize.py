"""
Define the REST verbs relative to the JWT tokens
"""

from flasgger import swag_from
from flask import make_response, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument
from util import parse_params
from util import ApiError
# from flask import current_app as app
from repositories import ClientRepository

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
        client = ClientRepository.getById(client_id, client_secret)
        if client:
            token = create_access_token(identity=client.slug)
            return make_response(jsonify(jwt=token), 200)
        else:
            return make_response(
                ApiError(
                    "Invalid credentials",
                    {"error": "The credentials provided are invalid"}
                ).get_response())
