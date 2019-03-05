
"""Abstract Interface for a Ticket Provider"""
class TicketProvider():

    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def getTracker(project_path):
        """ Get the details from the issue tracker at path """
        raise NotImplementedError

    @staticmethod
    def getMembers(project_path):
        """ Get the members associated to the project at path """
        raise NotImplementedError

    @staticmethod
    def addMember(project_path, user_id, level):
        """ Add a member to a tracker"""
        raise NotImplementedError


    @staticmethod
    def getTickets(project_path):
        """ Get all the tickets from a given project path """
        raise NotImplementedError

    @staticmethod
    def getTicket(project_path, ticket_id):
        """ Get details from a ticket given a project_path and ticket_id """
        raise NotImplementedError

    @staticmethod
    def getTicketDiscussion(project_path, ticket_id):
        """ Get the discussion thread associated to a ticket """
        raise NotImplementedError

    @staticmethod
    def getUserByExternalId(provider, external_id):
        """ Get a user by external_id """
        user = self.git.users.list(extern_uid=external_id, provider=provider)[0]
        return user

        
    @staticmethod
    def getUserByEmail(email):
        """ Get a user by email """
        user = self.git.users.list(email=email)[0]
        return user



    @staticmethod
    def createTicket(project_path, from_user, to_user, subject, body, labels=[]):
        """ Create a ticket on the given project path """
        raise NotImplementedError


    @staticmethod
    def subscribeTicket(project_path, ticket_id, user_id):
        """ Subscribe a user to a ticket """
        raise NotImplementedError


    @staticmethod
    def unsubscribeTicket(project_path, ticket_id, user_id):
        """ Subscribe a user to a ticket """
        raise NotImplementedError

    @staticmethod
    def listTicketComments(project_path, ticket_id):
        """ List all discussion on a ticket by ticket_id and project_path """
        raise NotImplementedError

    @staticmethod
    def commentTicket(project_path, ticket_id, comment_subject, comment_body):
        """ Comment a ticket """
        raise NotImplementedError