from models import Ticket
from bson import ObjectId
from service.user import UserService

class TicketService:
    @staticmethod
    def create_ticket(user_id, user_role, message):
        if user_role == "USER":
            Ticket.objects.create(user=user_id, messages=[message], state='NEW')
        else:
            admin_id = UserService.get_admin_id()
            Ticket.objects.create(user=user_id, messages=[message], state='WAITING', assignee_user_id=admin_id)

    @staticmethod
    def change_ticket_state(ticket_id, state):
        ticket = Ticket.objects.get({'_id': ObjectId(ticket_id)})
        ticket.state = state
        ticket.save()

    @staticmethod
    def add_message(ticket_id, username, message):
        print("3")
        ticket = Ticket.objects.get({'_id': ObjectId(ticket_id)})
        ticket.messages.append(username + ': ' + message)
        ticket.save()

    @staticmethod
    def change_state(ticket_id, new_state):
        ticket = Ticket.objects.get({'_id': ObjectId(ticket_id)})
        ticket.state = new_state
        ticket.save()

    @staticmethod
    def get_user_tickets(user_id):
        print(list(Ticket.objects.raw({'user': ObjectId(user_id)})))
        return list(Ticket.objects.raw({'user': ObjectId(user_id)}))

    @staticmethod
    def get_ticket_by_id(ticket_id):
        ticket = Ticket.objects.get({"_id": ObjectId(ticket_id)})
        return ticket
