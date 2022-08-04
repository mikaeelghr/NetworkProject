from models import Ticket


class TicketService:
    @staticmethod
    def create_ticket(username, message):
        Ticket.objects.create(username=username, messages=[message], state='NEW')

    @staticmethod
    def change_ticket_state(ticket_id, state):
        ticket = Ticket.objects.get({'_id': ticket_id})
        ticket.state = state
        ticket.save()

    @staticmethod
    def add_message(ticket_id, username, message):
        ticket = Ticket.objects.get({'_id': ticket_id})
        ticket.messages.append(username + ': ' + message)
        ticket.save()

    @staticmethod
    def get_user_tickets(username):
        return list(Ticket.objects.raw({'username': username}))