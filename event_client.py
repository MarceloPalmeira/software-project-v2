import requests

BASE_URL = "http://127.0.0.1:5000"

def create_event():
    name = input("Event name: ")
    date = input("Event date (YYYY-MM-DD): ")
    budget = input("Initial budget: ")
    response = requests.post(f"{BASE_URL}/create_event", data={"name": name, "date": date, "budget": budget})
    print(response.json())

def get_events():
    response = requests.get(f"{BASE_URL}/")
    events = response.json()
    if not events:
        print("No events registered.")
    else:
        for event in events:
            print(f"ID: {event['id']} | Name: {event['name']} | Date: {event['date']} | Budget: {event['budget']}")

def register_attendee():
    event_id = input("Event ID: ")
    name = input("Participant name: ")
    response = requests.post(f"{BASE_URL}/register_participant", data={"name": name, "event_id": event_id})
    print(response.json())

def get_attendees():
    response = requests.get(f"{BASE_URL}/attendees")
    print(response.json())

def register_speaker():
    event_id = input("Event ID: ")
    name = input("Speaker name: ")
    description = input("Description: ")
    response = requests.post(f"{BASE_URL}/register_speaker", data={"name": name, "description": description, "event_id": event_id})
    print(response.json())

def register_vendor():
    event_id = input("Event ID: ")
    name = input("Vendor name: ")
    services = input("Offered services: ")
    response = requests.post(f"{BASE_URL}/register_vendor", data={"name": name, "services": services, "event_id": event_id})
    print(response.json())

def update_budget():
    event_id = input("Event ID: ")
    amount = input("Amount to add to budget: ")
    response = requests.post(f"{BASE_URL}/update_budget", data={"event_id": event_id, "amount": amount})
    print(response.json())

def add_feedback():
    event_id = input("Event ID: ")
    feedback = input("Enter your feedback: ")
    response = requests.post(f"{BASE_URL}/add_feedback", data={"event_id": event_id, "feedback": feedback})
    print(response.json())

def edit_event():
    event_id = input("Event ID to edit: ")
    new_name = input("New event name: ")
    new_date = input("New event date (YYYY-MM-DD): ")
    new_budget = input("New budget: ")
    response = requests.post(f"{BASE_URL}/edit_event", data={"event_id": event_id, "name": new_name, "date": new_date, "budget": new_budget})
    print(response.json())

def delete_event():
    event_id = input("Event ID to delete: ")
    response = requests.post(f"{BASE_URL}/delete_event", data={"event_id": event_id})
    print(response.json())

def main():
    while True:
        print("\n===== MENU =====\n")

        print("Events Session:")
        print("1. Create event")
        print("2. List events")
        print("3. Edit event")
        print("4. Delete event\n")

        print("Participants Session:")
        print("5. Register participant")
        print("6. List participants\n")

        print("Speakers Session:")
        print("7. Register speaker\n")

        print("Vendors Session:")
        print("8. Register vendor\n")

        print("Budget Session:")
        print("9. Update budget\n")

        print("10. Exit\n")

        option = input("Choose an option: ")

        if option == "1":
            create_event()
        elif option == "2":
            get_events()
        elif option == "3":
            edit_event()
        elif option == "4":
            delete_event()
        elif option == "5":
            register_attendee()
        elif option == "6":
            get_attendees()
        elif option == "7":
            register_speaker()
        elif option == "8":
            register_vendor()
        elif option == "9":
            update_budget()
        elif option == "10":
            print("Exiting...")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
