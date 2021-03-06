import unittest
from models.abc import db
from server import server
from repositories import ChannelRepository
from util import test_client


class TestCors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = test_client(server)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testCors(self):
        ChannelRepository.create(
            slug='a-channel',
            title='test channel',
            path='/dummy/path'
        )
        response = self.client.get('/api/channel/a-channel')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('Access-Control-Allow-Origin'), '*')
