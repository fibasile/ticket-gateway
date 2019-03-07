import unittest
import json
from server import server
from models.abc import db
from repositories import ChannelRepository, GitlabProvider
from unittest.mock import MagicMock, Mock
from repositories import GitlabProvider, gitClient


class TestGitlabProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testClientSudo(self):
        git = gitClient(22)
        self.assertEquals(git.headers['Sudo'], 22)
        git = gitClient()
        self.assertNotIn('Sudo', git.headers.keys())
