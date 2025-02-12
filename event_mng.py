from event import Event

class EventMng:
    def __init__(self):
        self.events = []
        self.next_id = 1

    def create_event(self, name, date, budget=0):
        event = Event(self.next_id, name, date, budget)
        self.events.append(event)
        self.next_id += 1
        return event.to_dict()

    def list_events(self):
        return [event.to_dict() for event in self.events]

    def get_event_by_id(self, event_id):
        for event in self.events:
            if event.id == event_id:
                return event
        return None

    def edit_event(self, event_id, new_name, new_date, new_budget):
        event = self.get_event_by_id(event_id)
        if event:
            event.name = new_name
            event.date = new_date
            event.budget = new_budget
            return event.to_dict()
        return {"error": "Event not found"}

    def remove_event(self, event_id):
        for event in self.events:
            if event.id == event_id:
                self.events.remove(event)
                return {"message": f"Evento {event_id} removido com sucesso"}
        return {"error": "Event not found"}
