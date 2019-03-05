import unittest
import json

from server import server
from models.abc import db
from models import Channel
from repositories import ChannelRepository


class TestChannel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        """ The GET on `/application/channel` should return a channel """      
        ChannelRepository.create(slug='a-channel', title='test channel', path='/dummy/path')
        response = self.client.get('/api/channel/a-channel')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {'data': {'title': 'test channel','slug': 'a-channel', 'path': '/dummy/path'}}
        )
    def test_get_notfound(self):
        """ The GET on `/api/channel/<nonexistent>` should return 404 """
        response = self.client.get('/api/channel/unknown-channel')
        self.assertEqual(response.status_code, 404)
        