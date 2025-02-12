class SpeakersMng:
    def __init__(self):
        self.speakers = {}

    def register_speaker(self, event, name, description):
        if event.id not in self.speakers:
            self.speakers[event.id] = []
        self.speakers[event.id].append({"name": name, "description": description})
        event.speakers.append({"name": name, "description": description})

    def list_speakers(self, event):
        return self.speakers.get(event.id, [])
