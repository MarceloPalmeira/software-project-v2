# client/event_client.py
import requests

BASE_URL = "http://127.0.0.1:5000"

class EventClient:
    def __init__(self):
        self.base_url = BASE_URL

    def create_event(self):
        while True:
            name = input("Event Name: ")
            date = input("Event Date (DD-MM-YYYY): ")
            budget = input("Initial Budget: ")

            response = requests.post(
                f"{self.base_url}/create_event",
                json={"name": name, "date": date, "budget": budget}
            )
            self._handle_response(response)

            if response.status_code == 201:
                break

    def get_events(self):
        response = requests.get(f"{self.base_url}/events")
        self._handle_response(response)

    def edit_event(self):
        while True:
            event_id = input("Event ID to edit: ")
            if not event_id.isdigit():
                print("Error: Invalid event ID. Please enter a valid numeric ID.")
                continue

            new_name = input("New Event Name (leave blank to keep current): ")
            new_date = input("New Event Date (DD-MM-YYYY, leave blank to keep current): ")
            new_budget = input("New Budget (leave blank to keep current): ")

            payload = {"event_id": event_id}
            if new_name.strip():
                payload["name"] = new_name
            if new_date.strip():
                payload["date"] = new_date
            if new_budget.strip():
                payload["budget"] = new_budget

            response = requests.post(f"{self.base_url}/edit_event", json=payload)
            self._handle_response(response)
            break

    def delete_event(self):
        while True:
            event_id = input("Event ID to delete: ")
            if not event_id.isdigit():
                print("Error: Invalid event ID. Please enter a valid numeric ID.")
                continue

            response = requests.post(f"{self.base_url}/delete_event", json={"event_id": event_id})
            self._handle_response(response)
            break

    def register_attendee(self):
        while True:
            event_id = input("Event ID: ")
            if not event_id.isdigit():
                print("Error: Invalid event ID. Please enter a valid numeric ID.")
                continue

            name = input("Participant Name: ")
            response = requests.post(
                f"{self.base_url}/register_participant",
                json={"event_id": event_id, "name": name}
            )
            self._handle_response(response)
            break

    def get_attendees(self):
        while True:
            event_id = input("Event ID: ")
            if not event_id.isdigit():
                print("Error: Invalid event ID. Please enter a valid numeric ID.")
                continue

            response = requests.get(f"{self.base_url}/attendees", params={"event_id": event_id})
            self._handle_response(response)
            break

    def edit_participant(self):
        participant_id = input("Participant ID: ")
        new_name = input("New Participant Name (leave blank to keep current): ")
        payload = {"participant_id": participant_id}
        if new_name.strip():
            payload["new_name"] = new_name

        response = requests.post(f"{self.base_url}/edit_participant", json=payload)
        self._handle_response(response)

    def register_speaker(self):
        while True:
            event_id = input("Event ID: ")
            if not event_id.isdigit():
                print("Error: Invalid event ID. Please enter a valid numeric ID.")
                continue

            name = input("Speaker Name: ")
            description = input("Description: ")
            response = requests.post(
                f"{self.base_url}/register_speaker",
                json={"event_id": event_id, "name": name, "description": description}
            )
            self._handle_response(response)
            break

    def list_speakers(self):
        while True:
            event_id = input("Event ID: ")
            if not event_id.isdigit():
                print("Error: Invalid event ID. Please enter a valid numeric ID.")
                continue

            response = requests.get(f"{self.base_url}/list_speakers", params={"event_id": event_id})
            self._handle_response(response)
            break

    def edit_speaker(self):
        speaker_id = input("Speaker ID: ")
        new_name = input("New Speaker Name (leave blank to keep current): ")
        new_description = input("New Description (leave blank to keep current): ")
        payload = {"speaker_id": speaker_id}
        if new_name.strip():
            payload["new_name"] = new_name
        if new_description.strip():
            payload["new_description"] = new_description

        response = requests.post(f"{self.base_url}/edit_speaker", json=payload)
        self._handle_response(response)

    def register_vendor(self):
        while True:
            event_id = input("Event ID: ")
            if not event_id.isdigit():
                print("Error: Invalid event ID. Please enter a valid numeric ID.")
                continue

            name = input("Vendor Name: ")
            services = input("Offered Services: ")
            response = requests.post(
                f"{self.base_url}/register_vendor",
                json={"event_id": event_id, "name": name, "services": services}
            )
            self._handle_response(response)
            break

    def list_vendors(self):
        while True:
            event_id = input("Event ID: ")
            if not event_id.isdigit():
                print("Error: Invalid event ID. Please enter a valid numeric ID.")
                continue

            response = requests.get(f"{self.base_url}/list_vendors", params={"event_id": event_id})
            self._handle_response(response)
            break

    def edit_vendor(self):
        vendor_id = input("Vendor ID: ")
        new_name = input("New Vendor Name (leave blank to keep current): ")
        new_services = input("New Services (leave blank to keep current): ")
        payload = {"vendor_id": vendor_id}
        if new_name.strip():
            payload["new_name"] = new_name
        if new_services.strip():
            payload["new_services"] = new_services

        response = requests.post(f"{self.base_url}/edit_vendor", json=payload)
        self._handle_response(response)

    def update_budget(self):
        event_id = input("Event ID: ")
        amount = input("Amount to add to budget: ")

        try:
            int(event_id)
            int(amount)
        except ValueError:
            print("Error: Invalid input. Please enter valid numeric values.")
            return

        response = requests.post(
            f"{self.base_url}/update_budget",
            json={"event_id": event_id, "amount": amount}
        )
        self._handle_response(response)

    def get_budget(self):
        event_id = input("Event ID: ")

        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            return

        response = requests.get(f"{self.base_url}/get_budget", params={"event_id": event_id})
        self._handle_response(response)

    def edit_budget(self):
        event_id = input("Event ID: ")
        new_budget = input("New Budget: ")

        try:
            int(event_id)
            int(new_budget)
        except ValueError:
            print("Error: Invalid input. Please enter valid numeric values.")
            return

        response = requests.post(
            f"{self.base_url}/edit_budget",
            json={"event_id": event_id, "new_budget": new_budget}
        )
        self._handle_response(response)

    def add_feedback(self):
        event_id = input("Event ID: ")
        feedback = input("Enter your feedback: ")

        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            return

        response = requests.post(
            f"{self.base_url}/add_feedback",
            json={"event_id": event_id, "feedback": feedback}
        )
        self._handle_response(response)

    def _handle_response(self, response):
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text}")
        try:
            print(response.json())
        except Exception as e:
            print("Error decoding the response:", e)

    def main(self):
        while True:
            print("\n===== MENU =====\n")
            print("1. Create event")
            print("2. List events")
            print("3. Edit event")
            print("4. Delete event")
            print("5. Register participant")
            print("6. List participants")
            print("7. Edit participant")
            print("8. Register speaker")
            print("9. List speakers")
            print("10. Edit speaker")
            print("11. Register vendor")
            print("12. List vendors")
            print("13. Edit vendor")
            print("14. Increase budget")
            print("15. Get budget")
            print("16. Edit budget")
            print("17. Add feedback")
            print("18. Exit\n")
            
            option = input("Choose an option: ")

            options = {
                "1": self.create_event,
                "2": self.get_events,
                "3": self.edit_event,
                "4": self.delete_event,
                "5": self.register_attendee,
                "6": self.get_attendees,
                "7": self.edit_participant,
                "8": self.register_speaker,
                "9": self.list_speakers,
                "10": self.edit_speaker,
                "11": self.register_vendor,
                "12": self.list_vendors,
                "13": self.edit_vendor,
                "14": self.update_budget,
                "15": self.get_budget,
                "16": self.edit_budget,
                "17": self.add_feedback,
                "18": self.exit_program
            }

            if option in options:
                options[option]()
            else:
                print("Invalid option!")

    def exit_program(self):
        print("Exiting...")
        exit()

if __name__ == "__main__":
    client = EventClient()
    client.main()
