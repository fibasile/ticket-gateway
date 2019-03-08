import unittest
import yaml
from server import server
from models.abc import db
import os
import pytest
from repositories import ClientRepository


@pytest.mark.current
class TestClient(unittest.TestCase):
    """Tests for JWT Tokens and access control"""

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testGet(self):
        """ GET on /api/client should return an API client """
        ClientRepository.create("a-slug", "A Client")
        response = self.client.get('/api/client/a-slug')
        self.assertEqual(response.status_code, 200)
