"""
Define the Channel model
"""
from . import db
from .abc import BaseModel, MetaBaseModel

class Channel(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Channel model """
    __tablename__ = 'channel'

    slug = db.Column(db.String(300), primary_key=True)
    title = db.Column(db.String(300))
    path = db.Column(db.String(300))
    
    def __init__(self, slug, title, path):
        """ Create a new User """
        self.slug = slug
        self.title = title
        self.path = path