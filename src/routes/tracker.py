"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api
from util import API_ERRORS
from resources import TrackerResource


TRACKER_BLUEPRINT = Blueprint('tracker', __name__)
Api(TRACKER_BLUEPRINT, catch_all_404s=True, errors=API_ERRORS).add_resource(
    TrackerResource,
    '/channel/<string:slug>/tracker'
)