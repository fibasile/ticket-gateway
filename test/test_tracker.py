import unittest
import json

from server import server
from models.abc import db
from repositories import ChannelRepository, GitlabProvider
from unittest.mock import MagicMock

from util import test_client


class TestTracker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = test_client(server)
        cls._getTracker = GitlabProvider.getTracker

    def setUp(self):
        db.create_all()
        ChannelRepository.create(
            slug='a-channel', title='test channel', path='/dummy/path')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        GitlabProvider.getTracker = TestTracker._getTracker

    def test_get(self):
        """ The GET on `/application/channel` should return a channel """
        GitlabProvider.getTracker = MagicMock(name="getTracker")
        GitlabProvider.getTracker.return_value = {
            "title": "Some title"
        }
        response = self.client.get('/api/channel/a-channel/tracker')
        self.assertEqual(response.status_code, 200)
        GitlabProvider.getTracker.assert_called_with('/dummy/path')
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {'data': {'title': 'Some title'}}
        )
