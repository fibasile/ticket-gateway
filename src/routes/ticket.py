"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api
from util import API_ERRORS
from resources import TicketResource, TicketsResource


TICKET_BLUEPRINT = Blueprint('ticket', __name__)
api = Api(TICKET_BLUEPRINT, catch_all_404s=True, errors=API_ERRORS)

api.add_resource(
    TicketResource,
    '/channel/<string:slug>/tickets/<string:ticket_id>'
)

api.add_resource(
    TicketsResource,
    '/channel/<string:slug>/tickets'
)