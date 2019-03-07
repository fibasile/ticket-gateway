import unittest
import yaml
from server import server
from models.abc import db
from repositories import ChannelRepository, GitlabProvider
from unittest.mock import MagicMock, Mock
from repositories import GitlabProvider, gitClient
import os


class TestGitlabProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()
        with open(os.path.join(os.getcwd(), 'test/fixtures/channels.yml'), 'r') as fixture:
            data = yaml.load(fixture)
            for channel in data["channels"]:
                c = ChannelRepository.create(
                    channel['slug'], channel['title'], channel['path'])

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testClientSudo(self):
        """Invoking the gitClient with a user id correctly """
        """sets the Sudo header on the gitlab api client"""
        git = gitClient(22)
        self.assertEquals(git.headers['Sudo'], "22")
        git = gitClient()
        self.assertNotIn('Sudo', git.headers.keys())

    def testGetTracker(self):
        """Calling getTracker should return an existing tracker's """
        """key information"""
        c = ChannelRepository.get('fablabs-approval')
        tracker = GitlabProvider.getTracker(c.path)
        self.assertIsNotNone(tracker)
        self.assertEquals(tracker.path_with_namespace, "fablabs/approval")

    def testGetMembers(self):
        c = ChannelRepository.get('fablabs-approval')
        members = GitlabProvider.getMembers(c.path)
        self.assertIsNotNone(members)
        self.assertGreaterEqual(len(members), 1)
