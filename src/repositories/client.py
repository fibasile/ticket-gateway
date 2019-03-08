from models import Client
from util import ApiError
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort


class ClientRepository:
    """ The repository for the cleint model """

    @staticmethod
    def get(slug):
        """ Query a channel by slug """
        try:
            return Client.query.filter_by(
                slug=slug,
            ).one()
        except exc.NoResultFound:
            abort(404)

    @staticmethod
    def getById(client_id, client_secret):
        """ Query a channel by client_id and client_secret """
        try:
            return Client.query.filter_by(
                client_id=client_id,
                client_secret=client_secret,
            ).one()
        except exc.NoResultFound:
            abort(404)

    @staticmethod
    def create(slug, title, ):
        """ Create a new client """
        client = Client(slug, title)
        try:
            return client.save()
        except Exception as ex:
            abort(400)

    @staticmethod
    def delete(slug):
        """ Delete a client """
        raise NotImplementedError
