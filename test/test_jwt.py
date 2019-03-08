import unittest
from server import server
from models.abc import db
import pytest
from repositories import ClientRepository
import json


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

    def testLoginNotFound(self):
        """the POST on /api/authorize with invalid credentials should error"""
        response = self.client.post(
            '/api/authorize', json={"client_id": "dafdasf", "client_secret": "dafadsfasdf"})
        self.assertEqual(response.status_code, 404)

    def testLoginSuccess(self):
        """ the POST on /api/authorize with valid parameters """
        """ should generate a JWT Token """
        client = ClientRepository.create("test", "Test")
        self.assertIsNotNone(client.client_id)
        self.assertIsNotNone(client.client_secret)

        response = self.client.post(
            '/api/authorize', json={
                "client_id": client.client_id,
                "client_secret": client.client_secret}
        )

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(response_json["jwt"])
