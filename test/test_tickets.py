import unittest
import json

from server import server
from models.abc import db

from repositories import ChannelRepository, GitlabProvider
from unittest.mock import MagicMock

from util import test_client


class TestTickets(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = test_client(server)
        cls._getTracker = GitlabProvider.getTracker
        cls._getTickets = GitlabProvider.getTickets

    def setUp(self):
        db.create_all()
        ChannelRepository.create(
            slug='a-channel', title='test channel', path='/dummy/path')
        GitlabProvider.getTracker = MagicMock(name="getTracker")
        GitlabProvider.getTracker.return_value = {
            "title": "Some title",
            "id": "Some id"
        }
        GitlabProvider.getTickets = MagicMock(name="getTickets")
        GitlabProvider.getTickets.return_value = [{
            "id": "3243",
            "title": "Issue title"
        }]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        GitlabProvider.getTracker = TestTickets._getTracker
        GitlabProvider.getTicket = TestTickets._getTickets

    def test_get(self):
        """ The GET on `/application/channel/tickets` should return """
        """ a list of tickets for the channel """
        response = self.client.get('/api/channel/a-channel/tickets')
        self.assertEqual(response.status_code, 200)
        GitlabProvider.getTracker.assert_called_with('/dummy/path')
        GitlabProvider.getTickets.assert_called_with('/dummy/path')
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {'data': [{"id": "3243", 'title': 'Issue title'}]}
        )
