from .provider import TicketProvider
import gitlab
import config

git = gitlab.gitlab(config.GITLAB_URL, config.GITLAB_TOKEN)

class GitlabProvider(TicketProvider):

    @staticmethod
    def getTracker(project_path):
        """ Get the details from the issue tracker at path """
        project = git.projects.get(project_path)
        return project


    @staticmethod
    def getMembers(project_path):
        """ Get the members associated to the project at path """
        project =  getTracker(project_path)
        return project.members.all(all=True)


    @staticmethod
    def addMember(project_path, user_id, level):
        """ Add a member to a tracker"""
        tracker = getTracker(project_path)
        levels = { 'developer' : gitlab.DEVELOPER_ACCESS, 'master' : gitlab.MASTER_ACCESS }
        member = tracker.members.create({'user_id': user_id, 'access_level': levels[level]})
        return member

    @staticmethod
    def getTickets(project_path):
        """ Get all the tickets from a given project path """
        tracker = getTracker(project_path)
        issues = tracker.issues.list(all=True)
        return issues

    @staticmethod
    def getTicket(project_path, ticket_id):
        """ Get details from a ticket given a project_path and ticket_id """
        tracker = getTracker(project_path)
        issue = tracker.issues.get(ticket_id)
        return issue

    @staticmethod
    def getTicketDiscussion(project_path, ticket_id):
        """ Get the discussion thread associated to a ticket """
        tracker = getTracker(project_path)
        issue = tracker.issues.get(ticket_id)
        return issue.notes.list(all=True)

    @staticmethod
    def addTicketDiscussion(project_path, ticket_id, user_id,body):
        """ Add a new comment to the ticket """
        issue = tracker.issues.get(ticket_id)
        ## TODO Do as user
        git.headers['Sudo']=user_id
        note = issue.notes.create({body: body})
        del git.headers['Sudo']
        return note

    @staticmethod
    def getUserByExternalId(provider, external_id):
        """ Get a user by external_id """
        user = git.users.list(extern_uid=external_id, provider=provider)[0]
        return user

    @staticmethod
    def getUserByEmail(email):
        """ Get a user by email """
        user = git.users.list(email=email)[0]
        return user

    @staticmethod
    def createTicket(project_path, from_user, to_user, subject, body, labels=[]):
        """ Create a ticket on the given project path """
        tracker = getTracker(project_path)
        from_user = getUser(from_user)
        to_user = getUser(to_user)
        git.headers['Sudo']=from_user.id
        ticket = tracker.issues.create({ "title" : subject, "description" : body })
        del git.headers['Sudo']
        return ticket