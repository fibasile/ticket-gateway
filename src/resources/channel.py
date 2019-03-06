"""
Define the REST verbs relative to the channels
"""

from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask.json import jsonify
from repositories import ChannelRepository
from util import parse_params


class ChannelResource(Resource):
    """ Verbs relative to the users """
    @staticmethod
    @swag_from('../swagger/channel/GET.yml')
    def get(slug):
        """ Return an channel key information based on his slug """        
        channel = ChannelRepository.get(slug=slug)
        return jsonify({'data': channel.json})

    @staticmethod
    @parse_params(

        Argument(
            'title',
            location='json',
            required=True,
            help='The title for this channel'
        ),
        Argument(
            'path',
            location='json',
            required=True,
            help='The path of this channel on the hosting platform'
        )
    )
    @swag_from('../swagger/channel/POST.yml')
    def post(slug, title, path):
        """ Create an user based on the sent information """
        channel = ChannelRepository.create(
            slug=slug,
            title=title,
            path=path
        )
        r = jsonify({'data': channel.json})
        r.status_code = 201
        return r

 