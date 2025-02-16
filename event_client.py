import requests

BASE_URL = "http://127.0.0.1:5000"

def create_event():
    name = input("Event name: ")
    date = input("Event date (DD-MM-YYYY): ")
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
    
def list_speakers():
    event_id = input("Event ID: ")
    response = requests.get(f"{BASE_URL}/list_speakers", params={"event_id": event_id})
    print(response.json())

def edit_speaker():
    event_id = input("Event ID: ")
    old_name = input("Nome atual do speaker: ")
    new_name = input("Novo nome do speaker: ")
    new_description = input("Nova descrição: ")
    response = requests.post(f"{BASE_URL}/edit_speaker", data={
        "event_id": event_id,
        "old_name": old_name,
        "new_name": new_name,
        "new_description": new_description
    })
    print(response.json())

def list_vendors():
    event_id = input("Event ID: ")
    response = requests.get(f"{BASE_URL}/list_vendors", params={"event_id": event_id})
    print(response.json())

def edit_vendor():
    event_id = input("Event ID: ")
    old_name = input("Nome atual do vendor: ")
    new_name = input("Novo nome do vendor: ")
    new_services = input("Novos serviços: ")
    response = requests.post(f"{BASE_URL}/edit_vendor", data={
        "event_id": event_id,
        "old_name": old_name,
        "new_name": new_name,
        "new_services": new_services
    })
    print(response.json())

def get_budget():
    event_id = input("Event ID: ")
    response = requests.get(f"{BASE_URL}/get_budget", params={"event_id": event_id})
    print(response.json())

def edit_budget():
    event_id = input("Event ID: ")
    new_budget = input("Novo budget: ")
    response = requests.post(f"{BASE_URL}/edit_budget", data={
        "event_id": event_id,
        "new_budget": new_budget
    })
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
        print("7. Register speaker")
        print("8. List speakers")
        print("9. Edit speaker\n")
        
        print("Vendors Session:")
        print("10. Register vendor")
        print("11. List vendors")
        print("12. Edit vendor\n")
        
        print("Budget Session:")
        print("13. Increase budget")
        print("14. Get budget")
        print("15. Edit budget\n")
        
        print("Feedback:")
        print("16. Add feedback\n")
        
        print("17. Exit\n")
        
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
            list_speakers()
        elif option == "9":
            edit_speaker()
        elif option == "10":
            register_vendor()
        elif option == "11":
            list_vendors()
        elif option == "12":
            edit_vendor()
        elif option == "13":
            update_budget()
        elif option == "14":
            get_budget()
        elif option == "15":
            edit_budget()
        elif option == "16":
            add_feedback()
        elif option == "17":
            print("Exiting...")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
