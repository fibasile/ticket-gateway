import unittest
import json
from server import server
from models.abc import db
from repositories import ChannelRepository, GitlabProvider
from unittest.mock import MagicMock, Mock
# from flask import make_response
# from flask.json import jsonify


class TestDiscussions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()
        cls._getTicket = GitlabProvider.getTicket
        cls._addTicketDiscussion = GitlabProvider.addTicketDiscussion
        cls._createTicketDiscussion = GitlabProvider.createTicketDiscussion

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
        cls = TestDiscussions
        GitlabProvider.getTicket = cls._getTicket
        GitlabProvider.addTicketDiscussion = cls._addTicketDiscussion
        GitlabProvider.createTicketDiscussion = cls._createTicketDiscussion

    def test_get(self):
        """The GET on `/api/channel/a-channel/tickets/ticket_id/discussions`"""

        GitlabProvider.getTicket = MagicMock()
        GitlabProvider.getTicket.return_value = Mock(
            discussions=Mock(list=Mock(return_value=[
                {"id": "3243", "title": "test"}
            ])))
        response = self.client.get(
            '/api/channel/a-channel/tickets/some_ticket/discussions')
        self.assertEqual(response.status_code, 200)

        GitlabProvider.getTicket.assert_called_with(
            '/dummy/path', 'some_ticket')
        # GitlabProvider.getMembers.assert_called_with('/dummy/path')
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {'data': [{"id": "3243", "title": "test"}]}
        )

    def test_post_new(self):
        """POST on `/api/channel/a-channel/tickets/ticket_id/discussions`"""
        """should create a comment in a bew discussion """
        GitlabProvider.addTicketDiscussion = MagicMock(
            name="addTicketDiscussion")
        GitlabProvider.addTicketDiscussion.return_value = {"status": "success"}
        response = self.client.post(
            '/api/channel/a-channel/tickets/some_ticket/discussions',
            json={
                "discussion_id": "3232",
                "user_id": "3234",
                "body": "Some comment"
            })
        self.assertEqual(response.status_code, 201)
        GitlabProvider.addTicketDiscussion.assert_called_with(
            '/dummy/path', 'some_ticket', '3232', '3234', 'Some comment')

    def test_post_existing(self):
        """POST on `/api/channel/a-channel/tickets/ticket_id/discussions`"""
        """should create a comment in an existing discussion """
        GitlabProvider.createTicketDiscussion = MagicMock(
            name="createTicketDiscussion")
        GitlabProvider.createTicketDiscussion.return_value = {
            "status": "success"}
        response = self.client.post(
            '/api/channel/a-channel/tickets/some_ticket/discussions',
            json={
                "user_id": "3234",
                "body": "Some comment"
            })
        self.assertEqual(response.status_code, 201)
        GitlabProvider.createTicketDiscussion.assert_called_with(
            '/dummy/path', 'some_ticket',  '3234', 'Some comment')
