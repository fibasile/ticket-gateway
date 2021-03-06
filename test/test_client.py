import unittest

from server import server
from models.abc import db
from models import Client
import pytest
from repositories import ClientRepository
from util import test_client


@pytest.mark.current
class TestClient(unittest.TestCase):
    """Tests for JWT Tokens and access control"""

    @classmethod
    def setUpClass(cls):
        cls.client = test_client(server)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testModel(self):
        client = ClientRepository.create("test", "Test")
        self.assertIsNotNone(client.client_id)
        self.assertIsNotNone(client.client_secret)

    def testGet(self):
        """ GET on /api/client should return an API client """
        ClientRepository.create("a-slug", "A Client")
        response = self.client.get('/api/client/a-slug')
        self.assertEqual(response.status_code, 200)
