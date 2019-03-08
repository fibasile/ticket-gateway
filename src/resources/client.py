"""
Define the REST verbs relative to the channels
"""

from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask.json import jsonify
from repositories import ClientRepository
from util import parse_params


class ClientResource(Resource):
    """ Verbs relative to the clients """
    @staticmethod
    @swag_from('../swagger/client/GET.yml')
    def get(slug):
        """ Return a client key information based on his slug """
        channel = ClientRepository.get(slug=slug)
        return jsonify({'data': channel.json})

    @staticmethod
    @parse_params(
        Argument(
            'title',
            location='json',
            required=True,
            help='The title for this channel'
        )
    )
    @swag_from('../swagger/client/POST.yml')
    def post(slug, title):
        """ Create a client based on the sent information """
        channel = ClientRepository.create(
            slug=slug,
            title=title
        )
        r = jsonify({'data': channel.json})
        r.status_code = 201
        return r
