"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api
from util import API_ERRORS
from resources import MembersResource


MEMBERS_BLUEPRINT = Blueprint('members', __name__)
api = Api(MEMBERS_BLUEPRINT, catch_all_404s=True, errors=API_ERRORS)

# api.add_resource(
#     TicketResource,
#     '/channel/<string:slug>/tickets/<string:ticket_id>'
# )

api.add_resource(
    MembersResource,
    '/channel/<string:slug>/members'
)