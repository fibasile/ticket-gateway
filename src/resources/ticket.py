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
from flask_jwt_extended import jwt_required


class TicketResource(Resource):
    """ Verbs relative to the users """
    @staticmethod
    @jwt_required
    @swag_from('../swagger/ticket/GET.yml')
    def get(slug, ticket_id):
        """ Return an channel key information based on his slug """
        channel = ChannelRepository.get(slug)
        tracker = GitlabProvider.getTracker(channel.path)
        ticket = GitlabProvider.getTicket(channel.path, ticket_id)
        return jsonify({"data": ticket})
