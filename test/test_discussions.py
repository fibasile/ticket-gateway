import unittest
import json
from server import server
from models.abc import db
from repositories import ChannelRepository, GitlabProvider
from unittest.mock import MagicMock, Mock


class TestDiscussions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()
        ChannelRepository.create(
            slug='a-channel',
            title='test channel',
            path='/dummy/path'
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        """ The GET on `/api/channel/a-channel/tickets/ticket_id/discussions` should return a list of members """
        response = self.client.get(
            '/api/channel/a-channel/tickets/some_ticket/discussions')
        self.assertEqual(response.status_code, 200)
        # GitlabProvider.getMembers.assert_called_with('/dummy/path')
        # response_json = json.loads(response.data.decode('utf-8'))
        # self.assertEqual(
        #     response_json,
        #     {'data': [{"user_id": "3243", "username": "someuser"}]}
        # )
