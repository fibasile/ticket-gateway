"""
Define the Channel model
"""
from . import db
from .abc import BaseModel, MetaBaseModel
from binascii import hexlify
import os

KEY_LENGTH = 64


class Client(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Channel model """
    __tablename__ = 'client'

    slug = db.Column(db.String(300), primary_key=True)
    title = db.Column(db.String(300), nullable=True)
    client_id = db.Column(db.String(300), nullable=False)
    client_secret = db.Column(db.String(300), nullable=False)

    def __init__(self, slug, title, client_id=None, client_secret=None):
        """ Create a new Client """
        self.slug = slug
        self.title = title
        self.client_id = client_id
        self.client_secret = client_secret
        if not client_id:
            self.client_id = self.randomHex()
        if not client_secret:
            self.client_secret = self.randomHex()

    @staticmethod
    def randomHex():
        key = hexlify(os.urandom(KEY_LENGTH))
        return key
