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


class DiscussionsResource(Resource):
    """ Verbs relative to the discussions """
    @staticmethod
    @swag_from('../swagger/discussions/GET.yml')
    def get(slug, ticket_id):
        """ Return an channel key information based on his slug """
        channel = ChannelRepository.get(slug)
        ticket = GitlabProvider.getTicket(channel.path, ticket_id)
        discussions = ticket.discussions.list(all=True)
        return jsonify({"data": discussions})
