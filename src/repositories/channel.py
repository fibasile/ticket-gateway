from models import Channel
from util import ApiError
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort


class ChannelRepository:
    """ The repository for the channel model """

    @staticmethod
    def get(slug):
        """ Query a channel by slug """
        try:
            return Channel.query.filter_by(
                slug=slug,
            ).one()
        except exc.NoResultFound:
            abort(404)

    @staticmethod
    def create(slug, title, path):
        """ Create a new channel """
        channel = Channel(slug, title, path)
        try:
            return channel.save()
        except Exception as ex:
            abort(400)
