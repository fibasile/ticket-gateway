import unittest
import yaml
from server import server
from models.abc import db
import os
import pytest


@pytest.mark.current
class TestJWT(unittest.TestCase):
    """Tests for JWT Tokens and access control"""

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testLogin(self):
        """the POST on /api/authorize should generate a valid JWT Token"""
        response = self.client.post(
            '/api/authorize', json={"client_id": "", "client_secret": ""})
        self.assertEquals(response.status_code, 400)
