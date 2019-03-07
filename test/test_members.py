import unittest
import json
from server import server
from models.abc import db
from repositories import ChannelRepository, GitlabProvider
from unittest.mock import MagicMock, Mock


class TestMembers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()
        ChannelRepository.create(
            slug='a-channel', title='test channel', path='/dummy/path')
        GitlabProvider.getTracker = MagicMock(name="getTracker")
        GitlabProvider.getTracker.return_value = {
            "title": "Some title",
            "id": "Some id"
        }
        GitlabProvider.getMembers = MagicMock(name="getMembers")
        GitlabProvider.getMembers.return_value = [{
            "user_id": "3243",
            "username": "someuser"
        }]

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        """ The GET on `/api/channel/a-channel/members` should return a list of members """
        response = self.client.get('/api/channel/a-channel/members')
        self.assertEqual(response.status_code, 200)
        GitlabProvider.getMembers.assert_called_with('/dummy/path')
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {'data': [{"user_id": "3243", "username": "someuser"}]}
        )

    def test_post(self):
        """ The POST on `/api/channel/a-channel/members` adds a member with valid params"""
        GitlabProvider.addMember = MagicMock(name="addMember")

        GitlabProvider.addMember.return_value = [{
            "status": "ok"
        }]
        response = self.client.post('/api/channel/a-channel/members', json={
            "user_id": "3243",
            "level": "master"
        })
        self.assertEqual(response.status_code, 200)
        GitlabProvider.addMember.assert_called_with(
            '/dummy/path', "3243", "master")

    def test_post_invalid_params(self):
        """ The POST on `/api/channel/a-channel/members` trows an error with"""
        """ invalid params """
        GitlabProvider.addMember = Mock(
            name="addMember", side_effect=Exception)
        response = self.client.post('/api/channel/a-channel/members', json={
            "user_id": "3243"
        })
        self.assertEqual(response.status_code, 400)
        GitlabProvider.addMember.assert_not_called()
