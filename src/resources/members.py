"""
Define the REST verbs relative to the trackers
"""

from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask.json import jsonify
from repositories import ChannelRepository
from repositories import GitlabProvider
from util import parse_params
from util import ApiError


class MembersResource(Resource):
    """ Verbs relative to the users """
    @staticmethod
    @swag_from('../swagger/members/GET.yml')
    def get(slug):
        """ Return an channel key information based on his slug """
        channel = ChannelRepository.get(slug)
        members = GitlabProvider.getMembers(channel.path)
        return jsonify({"data": members})

    @staticmethod
    @swag_from('../swagger/members/POST.yml')
    @parse_params(
        Argument(
            'user_id',
            location='json',
            required=True,
            help='The user id of the new member'
        ),
        Argument(
            'level',
            location='json',
            required=True,
            help='The access level developer or master'
        )
    )
    def post(slug, user_id, level="developer"):
        """Add a member to the channel"""
        channel = ChannelRepository.get(slug)
        response = jsonify(status="success")
        try:
            GitlabProvider.addMember(channel.path, user_id, level)
        except:
            response = ApiError("Bad Request",
                                {"error": "Invalid request data"}).get_response()
        return response
