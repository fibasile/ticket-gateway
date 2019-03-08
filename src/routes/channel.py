"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api
from util import API_ERRORS
from resources import ChannelResource


CHANNEL_BLUEPRINT = Blueprint('channel', __name__)
Api(CHANNEL_BLUEPRINT, catch_all_404s=True, errors=API_ERRORS).add_resource(
    ChannelResource,
    '/channel/<string:slug>'
)
