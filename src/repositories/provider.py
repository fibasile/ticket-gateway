
"""Abstract Interface for a Ticket Provider"""


class TicketProvider():

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def getTracker(cls, project_path):
        """ Get the details from the issue tracker at path """
        raise NotImplementedError

    @classmethod
    def getMembers(cls, project_path):
        """ Get the members associated to the project at path """
        raise NotImplementedError

    @classmethod
    def addMember(cls, project_path, user_id, level):
        """ Add a member to a tracker"""
        raise NotImplementedError

    @classmethod
    def getTickets(cls, project_path):
        """ Get all the tickets from a given project path """
        raise NotImplementedError

    @classmethod
    def getTicket(cls, project_path, ticket_id):
        """ Get details from a ticket given a project_path and ticket_id """
        raise NotImplementedError

    @classmethod
    def getTicketDiscussion(cls, project_path, ticket_id):
        """ Get the discussion thread associated to a ticket """
        raise NotImplementedError

    @classmethod
    def getUserByExternalId(cls, provider, external_id):
        """ Get a user by external_id """
        raise NotImplementedError

    @classmethod
    def getUserByEmail(cls, email):
        """ Get a user by email """
        raise NotImplementedError

    @classmethod
    def createTicket(cls,
                     project_path,
                     from_user,
                     to_user,
                     subject,
                     body,
                     labels=[]):
        """ Create a ticket on the given project path """
        raise NotImplementedError

    @classmethod
    def subscribeTicket(cls, project_path, ticket_id, user_id):
        """ Subscribe a user to a ticket """
        raise NotImplementedError

    @classmethod
    def unsubscribeTicket(cls, project_path, ticket_id, user_id):
        """ Subscribe a user to a ticket """
        raise NotImplementedError

    @classmethod
    def listTicketComments(cls, project_path, ticket_id):
        """ List all discussion on a ticket by ticket_id and project_path """
        raise NotImplementedError

    @classmethod
    def commentTicket(cls, project_path,
                      ticket_id,
                      comment_subject,
                      comment_body):
        """ Comment a ticket """
        raise NotImplementedError
