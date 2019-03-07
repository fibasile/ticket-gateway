"""
Define the REST verbs relative to the trackers
"""

from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask.json import jsonify
from flask import make_response
from repositories import ChannelRepository
from repositories import GitlabProvider
from util import parse_params
from util import ApiError
# from flask import current_app as app


class DiscussionsResource(Resource):
    """ Verbs relative to the discussions """

    @staticmethod
    @swag_from('../swagger/discussions/GET.yml')
    def get(slug, ticket_id):
        """ Return an channel key information based on his slug """
        # app.logger.debug("Getting ticket %s discussions" % ticket_id)
        channel = ChannelRepository.get(slug)
        ticket = GitlabProvider.getTicket(channel.path, ticket_id)
        discussions = ticket.discussions.list(all=True)
        return jsonify(dict({"data": discussions}))

    @staticmethod
    @swag_from('../swagger/members/POST.yml')
    @parse_params(
        Argument(
            'body',
            location='json',
            required=True,
            help='The body of the new comment'
        ),
        Argument(
            'user_id',
            location="json",
            required=True,
            help='User id of the author of the new comment'
        ),
        Argument(
            'discussion_id',
            location="json",
            help='Optional id of an existing discussion'
        )
    )
    def post(slug, ticket_id, user_id, body, discussion_id=None):
        """Add a comment to a ticket_id starting a discussion"""
        channel = ChannelRepository.get(slug)
        try:
            if discussion_id:
                # app.logger.debug("Adding to discussion %s for %s by %s: %s" %
                #                  (discussion_id, ticket_id, user_id, body))

                GitlabProvider.addTicketDiscussion(
                    channel.path, ticket_id, discussion_id, user_id, body)
            else:
                # app.logger.debug("Creating discussion for %s by %s: %s" %
                #                  (ticket_id, user_id, body))
                GitlabProvider.createTicketDiscussion(
                    channel.path, ticket_id, user_id, body)
            return make_response(jsonify(message='Comment created'), 201)
        except:
            response = ApiError("Bad Request",
                                {"error": "Invalid request data"}
                                ).get_response()
            return response
