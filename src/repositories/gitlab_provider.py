from .provider import TicketProvider
import gitlab
import os
GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.fabcloud.org')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')


def gitClient(sudo=None):

    git = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN, api_version=4)
    if sudo:
        git.headers['Sudo'] = str(sudo)
    git.auth()
    return git


class GitlabProvider(TicketProvider):

    @classmethod
    def getTracker(cls, project_path, sudo=None):
        """ Get the details from the issue tracker at path """
        git = gitClient(sudo)
        project = git.projects.get(project_path)
        return project

    @classmethod
    def getMembers(cls, project_path):
        """ Get the members associated to the project at path """
        project = cls.getTracker(project_path)
        return project.members.list(all=True)

    @classmethod
    def addMember(cls, project_path, user_id, level):
        """ Add a member to a tracker"""
        tracker = cls.getTracker(project_path)
        levels = {
            'developer': gitlab.DEVELOPER_ACCESS,
            'master': gitlab.MASTER_ACCESS
        }
        member = tracker.members.create(
            {'user_id': user_id, 'access_level': levels[level]})
        return member

    @classmethod
    def removeMember(cls, project_path, user_id):
        """ Remove a member from the tracker """
        tracker = cls.getTracker(project_path)
        member = tracker.members.get(user_id)
        member.delete()
        return None

    @classmethod
    def getTickets(cls, project_path):
        """ Get all the tickets from a given project path """
        tracker = cls.getTracker(project_path)
        issues = tracker.issues.list(all=True)
        return issues

    @classmethod
    def getTicket(cls, project_path, ticket_id):
        """ Get details from a ticket given a project_path and ticket_id """
        tracker = cls.getTracker(project_path)
        issue = tracker.issues.get(ticket_id)
        return issue

    @classmethod
    def getTicketDiscussion(cls, project_path, ticket_id):
        """ Get the discussion thread associated to a ticket """
        tracker = cls.getTracker(project_path)
        issue = tracker.issues.get(ticket_id)
        return issue.notes.list(all=True)

    @classmethod
    def addTicketDiscussion(cls, project_path, ticket_id,
                            discussion_id,  user_id, body):
        """ Add a new comment to the ticket """
        tracker = cls.getTracker(project_path, user_id)
        issue = tracker.issues.get(ticket_id)
        discussion = issue.discussions.get(discussion_id)
        note = discussion.notes.create({"body": body})
        return note

    @classmethod
    def createTicketDiscussion(cls, project_path, ticket_id, user_id, body):
        """ Add a new comment to the ticket """
        tracker = cls.getTracker(project_path, user_id)
        issue = tracker.issues.get(ticket_id)
        discussion = issue.discussions.create({"body": body})
        return discussion

    @classmethod
    def getUserByExternalId(cls, provider, external_id):
        """ Get a user by external_id """
        git = gitClient()
        user = git.users.list(
            query_parameters={
                "extern_uid": external_id,
                "provider": provider}
        )[0]
        return user

    @classmethod
    def getUserByUsername(cls, username):
        """ Get a user by email """
        git = gitClient()
        user = git.users.list(username=username)[0]
        return user

    @classmethod
    def getUserById(cls, user_id):
        """ Get a user by id """
        git = gitClient()
        user = git.users.get(user_id)
        return user

    @classmethod
    def createTicket(cls,
                     project_path,
                     from_user,
                     to_user,
                     subject,
                     body,
                     labels=[]
                     ):
        """ Create a ticket on the given project path """
        tracker = cls.getTracker(project_path, from_user)

        ticket = tracker.issues.create(
            {"title": subject, "description": body})

        return ticket

    @classmethod
    def removeTicket(cls,
                     project_path, ticket_id):
        """ Remove a ticket at the given project path """
        tracker = cls.getTracker(project_path)
        issue = tracker.issues.get(ticket_id)
        issue.delete()

    @classmethod
    def closeTicket(cls,
                    project_path, ticket_id):
        """ Closes a ticket at a given project path """
        tracker = cls.getTracker(project_path)
        issue = tracker.issues.get(ticket_id)
        issue.state_event = 'close'
        issue.save()

    @classmethod
    def reopenTicket(cls,
                     project_path, ticket_id):
        """ Reopen a ticket at a given project path """
        tracker = cls.getTracker(project_path)
        issue = tracker.issues.get(ticket_id)
        issue.state_event = 'reopen'
        issue.save()

    @classmethod
    def subscribeTicket(
        cls, project_path, ticket_id, user_id
    ):
        """Subscribe a user to the ticket """
        tracker = cls.getTracker(project_path, user_id)
        issue = tracker.issues.get(ticket_id)
        issue.subscribe()

    @classmethod
    def unsubscribeTicket(cls, project_path, ticket_id, user_id):
        """Unsubscribe a user from the ticket"""
        tracker = cls.getTracker(project_path, user_id)
        issue = tracker.issues.get(ticket_id)
        issue.unsubscribe()
