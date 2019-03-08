import unittest
import json
from server import server
from models.abc import db
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
        """The GET on `/application/channel` should return a channel"""
        ChannelRepository.create(
            slug='a-channel',
            title='test channel',
            path='/dummy/path')
        response = self.client.get('/api/channel/a-channel')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {
                'data': {
                    'title': 'test channel',
                    'slug': 'a-channel',
                    'path': '/dummy/path'
                }
            }
        )

    def test_get_notfound(self):
        """The GET on `/api/channel/<nonexistent>` should return 404 """
        response = self.client.get('/api/channel/unknown-channel')
        self.assertEqual(response.status_code, 404)

    def test_empty_slug(self):
        """The GET on `/api/channel` should handle bad requests"""
        ChannelRepository.create(
            slug='a-channel',
            title='test channel',
            path='/dummy/path')
        response = self.client.get('/api/channel')
        self.assertEqual(response.status_code, 404)

    def test_duplicate(self):
        """The POST on `/api/channel` should not accept an existing slug"""
        ChannelRepository.create(
            slug='a-channel',
            title='test channel',
            path='/dummy/path')
        response = self.client.post('/api/channel/a-channel', json={
            'title': 'Some channel',
            'path': '/dummy/path'
        })
        self.assertEqual(response.status_code, 400)

    def test_post(self):
        """The POST on `/api/channel` should create a channel"""
        response = self.client.post('/api/channel/another-channel', json={
            'title': 'Some channel',
            'path': '/dummy/path'
        })
        self.assertEqual(response.status_code, 201)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_json, {
            'data': {
                'title': 'Some channel',
                'slug': 'another-channel',
                'path': '/dummy/path'
            }
        })
        obj = ChannelRepository.get('another-channel')
        self.assertEqual(obj.title, 'Some channel')
        self.assertEqual(obj.path, '/dummy/path')
