import unittest
from repositories import ClientRepository
from flask_jwt_extended import create_access_token
from server import server


class JWTTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()
        cls.context = server.app_context()

    def authClient(self):
        with self.context:
            token = create_access_token(identity='testclient')
            client = server.test_client(
                headers={'Authorization': 'Bearer %s' % token})
            return client
