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

    def edit_speaker(self, event, old_name, new_name, new_description):
        speakers_list = self.speakers.get(event.id, [])
        for speaker in speakers_list:
            if speaker["name"] == old_name:
                speaker["name"] = new_name
                speaker["description"] = new_description
                # Atualiza também na lista do evento
                for sp in event.speakers:
                    if sp["name"] == old_name:
                        sp["name"] = new_name
                        sp["description"] = new_description
                        break
                return True
        return False
