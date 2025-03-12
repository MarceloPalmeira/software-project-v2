import requests

BASE_URL = "http://127.0.0.1:5000"

def create_event():
    while True:
        name = input("Event Name: ")
        date = input("Event Date (DD-MM-YYYY): ")
        budget = input("Initial Budget: ")

        response = requests.post(f"{BASE_URL}/create_event", json={"name": name, "date": date, "budget": budget})
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text}")
        
        if response.status_code != 201:
            try:
                error_message = response.json()
                print(f"Error: {error_message['error']}")
            except Exception as e:
                print("Error: The response is not a valid JSON.", e)
            if "Date must be in DD-MM-YYYY format" in response.text:
                print("Please enter the date in the correct format (DD-MM-YYYY).")
                continue
            elif "Budget must be a valid number" in response.text:
                print("Please enter a valid number for the budget.")
                continue
            else:
                break
        else:
            try:
                print(response.json())
                break
            except Exception as e:
                print("Error: The response is not a valid JSON.", e)
                break

def update_budget():
    while True:
        event_id = input("Event ID: ")
        amount = input("Amount to add to budget: ")

        try:
            int(event_id)
            int(amount)
        except ValueError:
            print("Error: Invalid input. Please enter valid numeric values.")
            continue

        response = requests.post(f"{BASE_URL}/update_budget", json={"event_id": event_id, "amount": amount})
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text}")
        
        if response.status_code != 200:
            try:
                error_message = response.json()
                print(f"Error: {error_message['error']}")
            except Exception as e:
                print("Error: The response is not a valid JSON.", e)
            if "Amount must be a valid number" in response.text:
                print("Please enter a valid amount for the budget increase.")
                continue
            else:
                break
        else:
            try:
                print(response.json())
                break
            except Exception as e:
                print("Error: The response is not a valid JSON.", e)
                break

def get_events():
    response = requests.get(f"{BASE_URL}/events")
    try:
        events = response.json()
        if not events:
            print("No events registered.")
        else:
            for event in events:
                print(f"ID: {event['id']} | Name: {event['name']} | Date: {event['date']} | Budget: {event['budget']}")
    except Exception as e:
        print("Error getting events:", e)

def edit_event():
    while True:
        event_id = input("Event ID to edit: ")
        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            continue
        
        new_name = input("New Event Name (leave blank to keep current): ")
        new_date = input("New Event Date (DD-MM-YYYY, leave blank to keep current): ")
        new_budget = input("New Budget (leave blank to keep current): ")

        payload = {"event_id": event_id}
        if new_name.strip() != "":
            payload["name"] = new_name
        if new_date.strip() != "":
            payload["date"] = new_date
        if new_budget.strip() != "":
            payload["budget"] = new_budget

        response = requests.post(f"{BASE_URL}/edit_event", json=payload)
        try:
            print(response.json())
            break
        except Exception as e:
            print("Error: The response is not a valid JSON.", e)
            break

def delete_event():
    while True:
        event_id = input("Event ID to delete: ")
        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            continue
        
        response = requests.post(f"{BASE_URL}/delete_event", json={"event_id": event_id})
        try:
            print(response.json())
            break
        except Exception as e:
            print("Error: The response is not a valid JSON.", e)

def register_attendee():
    while True:
        event_id = input("Event ID: ")
        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            continue
        
        name = input("Participant Name: ")
        response = requests.post(f"{BASE_URL}/register_participant", json={"event_id": event_id, "name": name})
        try:
            print(response.json())
            break
        except Exception as e:
            print("Error: The response is not a valid JSON.", e)

def get_attendees():
    while True:
        event_id = input("Event ID: ")
        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            continue
        
        response = requests.get(f"{BASE_URL}/attendees", params={"event_id": event_id})
        try:
            print(response.json())
            break
        except Exception as e:
            print("Error: The response is not a valid JSON.", e)

def edit_participant():
    participant_id = input("Participant ID: ")
    new_name = input("New Participant Name (leave blank to keep current): ")
    payload = {"participant_id": participant_id}
    if new_name.strip() != "":
        payload["new_name"] = new_name

    response = requests.post(f"{BASE_URL}/edit_participant", json=payload)
    try:
        print(response.json())
    except Exception as e:
        print("Error decoding the response:", e)

def register_speaker():
    while True:
        event_id = input("Event ID: ")
        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            continue

        name = input("Speaker Name: ")
        description = input("Description: ")
        response = requests.post(f"{BASE_URL}/register_speaker", json={"event_id": event_id, "name": name, "description": description})
        try:
            print(response.json())
            break
        except Exception as e:
            print("Error: The response is not a valid JSON.", e)

def list_speakers():
    while True:
        event_id = input("Event ID: ")
        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            continue

        response = requests.get(f"{BASE_URL}/list_speakers", params={"event_id": event_id})
        try:
            print(response.json())
            break
        except Exception as e:
            print("Error: The response is not a valid JSON.", e)

def edit_speaker():
    speaker_id = input("Speaker ID: ")
    new_name = input("New Speaker Name (leave blank to keep current): ")
    new_description = input("New Description (leave blank to keep current): ")
    payload = {"speaker_id": speaker_id}
    if new_name.strip() != "":
        payload["new_name"] = new_name
    if new_description.strip() != "":
        payload["new_description"] = new_description

    response = requests.post(f"{BASE_URL}/edit_speaker", json=payload)
    try:
        print(response.json())
    except Exception as e:
        print("Error decoding the response:", e)

def register_vendor():
    while True:
        event_id = input("Event ID: ")
        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            continue

        name = input("Vendor Name: ")
        services = input("Offered Services: ")
        response = requests.post(f"{BASE_URL}/register_vendor", json={"event_id": event_id, "name": name, "services": services})
        try:
            print(response.json())
            break
        except Exception as e:
            print("Error: The response is not a valid JSON.", e)

def list_vendors():
    while True:
        event_id = input("Event ID: ")
        try:
            int(event_id)
        except ValueError:
            print("Error: Invalid event ID. Please enter a valid numeric ID.")
            continue

        response = requests.get(f"{BASE_URL}/list_vendors", params={"event_id": event_id})
        try:
            print(response.json())
            break
        except Exception as e:
            print("Error: The response is not a valid JSON.", e)

def edit_vendor():
    vendor_id = input("Vendor ID: ")
    new_name = input("New Vendor Name (leave blank to keep current): ")
    new_services = input("New Services (leave blank to keep current): ")
    payload = {"vendor_id": vendor_id}
    if new_name.strip() != "":
        payload["new_name"] = new_name
    if new_services.strip() != "":
        payload["new_services"] = new_services

    response = requests.post(f"{BASE_URL}/edit_vendor", json=payload)
    try:
        print(response.json())
    except Exception as e:
        print("Error: The response is not a valid JSON.", e)

def update_budget():
    event_id = input("Event ID: ")
    amount = input("Amount to add to budget: ")

    try:
        int(event_id)
        int(amount)
    except ValueError:
        print("Error: Invalid input. Please enter valid numeric values.")
        return

    response = requests.post(f"{BASE_URL}/update_budget", json={"event_id": event_id, "amount": amount})
    try:
        print(response.json())
    except Exception as e:
        print("Error: The response is not a valid JSON.", e)

def get_budget():
    event_id = input("Event ID: ")

    try:
        int(event_id)
    except ValueError:
        print("Error: Invalid event ID. Please enter a valid numeric ID.")
        return

    response = requests.get(f"{BASE_URL}/get_budget", params={"event_id": event_id})
    try:
        print(response.json())
    except Exception as e:
        print("Error: The response is not a valid JSON.", e)

def edit_budget():
    event_id = input("Event ID: ")
    new_budget = input("New Budget: ")

    try:
        int(event_id)
        int(new_budget)
    except ValueError:
        print("Error: Invalid input. Please enter valid numeric values.")
        return

    response = requests.post(f"{BASE_URL}/edit_budget", json={"event_id": event_id, "new_budget": new_budget})
    try:
        print(response.json())
    except Exception as e:
        print("Error: The response is not a valid JSON.", e)

def add_feedback():
    event_id = input("Event ID: ")
    feedback = input("Enter your feedback: ")

    try:
        int(event_id)
    except ValueError:
        print("Error: Invalid event ID. Please enter a valid numeric ID.")
        return

    response = requests.post(f"{BASE_URL}/add_feedback", json={"event_id": event_id, "feedback": feedback})
    try:
        print(response.json())
    except Exception as e:
        print("Error: The response is not a valid JSON.", e)

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
        print("6. List participants")
        print("7. Edit participant\n")
        print("Speakers Session:")
        print("8. Register speaker")
        print("9. List speakers")
        print("10. Edit speaker\n")
        print("Vendors Session:")
        print("11. Register vendor")
        print("12. List vendors")
        print("13. Edit vendor\n")
        print("Budget Session:")
        print("14. Increase budget")
        print("15. Get budget")
        print("16. Edit budget\n")
        print("Feedback:")
        print("17. Add feedback\n")
        print("18. Exit\n")
        
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
            edit_participant()
        elif option == "8":
            register_speaker()
        elif option == "9":
            list_speakers()
        elif option == "10":
            edit_speaker()
        elif option == "11":
            register_vendor()
        elif option == "12":
            list_vendors()
        elif option == "13":
            edit_vendor()
        elif option == "14":
            update_budget()
        elif option == "15":
            get_budget()
        elif option == "16":
            edit_budget()
        elif option == "17":
            add_feedback()
        elif option == "18":
            print("Exiting...")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
