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


class TrackerResource(Resource):
    """ Verbs relative to the users """
    @staticmethod
    @jwt_required
    @swag_from('../swagger/tracker/GET.yml')
    def get(slug):
        """ Return an channel key information based on his slug """
        channel = ChannelRepository.get(slug)
        tracker = GitlabProvider.getTracker(channel.path)
        return jsonify({'data': tracker})
