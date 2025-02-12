class ParticipantsMng:
    def __init__(self):
        self.participants = {}

    def register_participant(self, event, name):
        if event.id not in self.participants:
            self.participants[event.id] = []
        self.participants[event.id].append(name)
        event.attendees.append(name)

    def list_participants(self, event):
        return self.participants.get(event.id, [])
