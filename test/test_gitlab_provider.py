import unittest
import yaml
from server import server
from models.abc import db
from repositories import ChannelRepository, GitlabProvider
# from unittest.mock import MagicMock, Mock
from repositories import GitlabProvider, gitClient
import os
# from importlib import reload
# uncomment below to run the git test
# this will work if you create two users and the projects in the fixtures/channels.yml
# users:
# ticketbot
# ticketfriend
# tickettester


class TestGitlabProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()
        self.bot = GitlabProvider.getUserByUsername('ticketbot')
        self.friend = GitlabProvider.getUserByUsername('ticketfriend')
        with open(os.path.join(os.getcwd(), 'test/fixtures/channels.yml'), 'r') as fixture:
            data = yaml.load(fixture)
            self.channels = data['channels']
        for channel in self.channels:
            c = ChannelRepository.create(
                channel['slug'], channel['title'], channel['path'])
            for member in channel['members']:
                try:
                    GitlabProvider.addMember(channel['slug'], member, 'master')
                except:
                    pass

    def tearDown(self):
        # for channel in self.channels:

        #     for member in channel['members']:
        #         try:
        #             GitlabProvider.removeMember(channel['slug'], member)
        #         except:
        #             pass
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
        """Calling getMembers returns a tracker member's list"""
        c = ChannelRepository.get('fablabs-approval')
        members = GitlabProvider.getMembers(c.path)
        self.assertIsNotNone(members)
        self.assertGreaterEqual(len(members), 1)

    def testGetUser(self):
        """Calling getUser returns an existing user"""
        c = ChannelRepository.get('fablabs-approval')
        member = GitlabProvider.getUserByUsername('tickettester')
        self.assertIsNotNone(member)
        self.assertEquals(member.username, "tickettester")
        with self.assertRaises(Exception):
            GitlabProvider.getUserByUsername('abubububub')

    def testAddRemoveUser(self):
        """Calling  addMember adds a new member, and calling removeMember removes it"""
        c = ChannelRepository.get('fablabs-approval')
        member = GitlabProvider.getUserByUsername('tickettester')
        oldMembers = GitlabProvider.getMembers(c.path)
        GitlabProvider.addMember(c.path, member.id, 'master')
        newMembers = GitlabProvider.getMembers(c.path)
        self.assertGreater(len(newMembers), len(oldMembers))
        GitlabProvider.removeMember(c.path, member.id)
        moreMembers = GitlabProvider.getMembers(c.path)
        self.assertLess(len(moreMembers), len(newMembers))

    def testCreateIssue(self):
        """Calling createTicket should create a ticket, Calling removeTicket should remove it"""
        c = ChannelRepository.get('fablabs-approval')
        ticket = GitlabProvider.createTicket(
            c.path, self.bot.id, self.friend.id,
            "[NEW LAB] This lab was submitted",
            "More than you want to know ever about this lab")
        self.assertIsNotNone(ticket)
        self.assertIsNotNone(ticket.id)
        self.assertIsNotNone(ticket.iid)
        self.assertEquals(ticket.title, "[NEW LAB] This lab was submitted")
        tickets = GitlabProvider.getTickets(c.path)
        self.assertGreater(
            len([aticket for aticket in tickets if aticket.id == ticket.id]), 0)
        GitlabProvider.removeTicket(
            c.path, ticket.iid
        )
        tickets = GitlabProvider.getTickets(c.path)
        self.assertEqual(
            len([aticket for aticket in tickets if aticket.id == ticket.id]), 0)

    def testCommentIssue(self):
        """calling createTicketDiscussion creates a comment in the issue"""
        c = ChannelRepository.get('fablabs-approval')
        ticket = GitlabProvider.createTicket(
            c.path, self.bot.id, self.friend.id,
            "[NEW LAB] This a test issue as the lab was submitted",
            "More than you want to know ever about this lab")

        discussion = GitlabProvider.createTicketDiscussion(
            c.path, ticket.iid, self.bot.id, "Some comment to this awesome issue")

        # import pdb
        # pdb.set_trace()

        self.assertIsNotNone(discussion)
        self.assertIsNotNone(discussion.attributes["notes"][0])
        note = discussion.attributes["notes"][0]
        self.assertEquals(note["body"],  "Some comment to this awesome issue")
        self.assertEquals(note["author"]["id"], self.bot.id)

        discussions = [
            discussion for discussion in ticket.discussions.list(all=True)]
        self.assertEquals(len(discussions), 1)
        # except:
        #     pass
        GitlabProvider.removeTicket(
            c.path, ticket.iid
        )

    def testReplyIssue(self):
        """calling addTicketDiscussion creates a reply to a comment in the issue"""
        c = ChannelRepository.get('fablabs-approval')
        ticket = GitlabProvider.createTicket(
            c.path, self.bot.id, self.friend.id,
            "[NEW LAB] This a test issue as the lab was submitted",
            "More than you want to know ever about this lab")

        discussion = GitlabProvider.createTicketDiscussion(
            c.path, ticket.iid, self.bot.id, "Some comment to this awesome issue")

        note = GitlabProvider.addTicketDiscussion(
            c.path, ticket.iid, discussion.id, self.friend.id, "Some reply")

        self.assertIsNotNone(note)
        self.assertIsNotNone(note.attributes["body"])

        GitlabProvider.removeTicket(
            c.path, ticket.iid
        )

    def testSubscribe(self):
        """calling subscribeTicket adds the user to the issue watchers"""
        pass

    def testUnsubscribe(self):
        """calling unsubscribeTicket removes the user from the issue watchers"""
        pass

    def testGetUserById(self):
        """calling getuserbyid should return an user by its id"""
        user = GitlabProvider.getUserById(self.bot.id)
        self.assertEquals(user.id, self.bot.id)
        self.assertEquals(user.username, self.bot.username)

    def testGetUserByExternalId(self):
        """calling getUserByExternalId should return a user"""
        user = GitlabProvider.getUserByUsername("fibasile")
        identity = user.attributes["identities"][0]
        self.assertIsNotNone(identity)
        byExtId = GitlabProvider.getUserByExternalId(
            identity["provider"], identity["extern_uid"])
        self.assertEquals(user.id, byExtId.id)
        self.assertEquals(user.attributes, byExtId.attributes)
