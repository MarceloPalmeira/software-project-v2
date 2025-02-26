class Event:
    def __init__(self, event_id, name, date, budget=0):
        self.id = event_id
        self.name = name
        self.date = date
        self.attendees = []
        self.speakers = []
        self.vendors = []
        self.feedbacks = []
        self.budget = budget

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "attendees": self.attendees,
            "speakers": self.speakers,
            "vendors": self.vendors,
            "feedbacks": self.feedbacks,
            "budget": self.budget
        }
