# Event Manager Software

## How to Run the Project

### 1. Install Dependencies  
Make sure you have Python installed, then run:  
pip install flask requests

### 2. Start the Server  
Run the following command in your terminal:  
python app.py  
The server will start at:  
http://127.0.0.1:5000/

### 3. Run the Client  
Open another terminal and execute:  
python event_client.py

---

## Project Structure and Class Descriptions

The project is structured into six core classes that manage different aspects of the event management system:

1. Event()
   This class represents an event with attributes such as:
   - id: Unique identifier for the event.
   - name: The name of the event.
   - date: The scheduled date of the event.
   - attendees: A list of registered attendees.
   - speakers: A list of speakers or performers.
   - vendors: A list of registered vendors.
   - feedbacks: A collection of feedback from attendees.
   - budget: The financial budget allocated for the event.

2. EventMng()
   Manages all event-related operations, including:
   - Creating new events.
   - Editing event details.
   - Listing all registered events.
   - Deleting events.
   - Handling feedback for events.

3. ParticipantsMng()
   Handles attendee registration and management:
   - Registers a participant to an event.
   - Retrieves a list of all attendees for a given event.

4. SpeakersMng()
   Manages speakers and performers at an event:
   - Registers a speaker with a description of their role.
   - Lists all registered speakers and performers for an event.
   - Edits a Speaker/Performer: Updates the speaker's name and description.
     If no new value is provided during editing (i.e. the field is left blank), the original information remains unchanged.

5. VendorsMng()
   Handles vendor registration and services:
   - Registers vendors who provide services or products.
   - Lists all vendors associated with a particular event.
   - Edits a Vendor: Updates the vendor's name and services.
     If no new value is provided during editing, the original information remains unchanged.

6. BudgetandFinancialMng()
   Manages the financial aspects of events:
   - Updates the Budget: Increases the event's budget by a specified amount.
   - Views the Current Budget.
   - Edits the Budget: Overwrites the event's budget with a new value.
     If no new value is provided during editing, the original budget remains unchanged.

---

## Features

Event Management:
- Create an Event: Adds an event by providing its name, date, and initial budget.
- Edit an Event: Modifies event details, including name, date, and budget.
- List Events: Displays all registered events.
- Delete an Event: Removes an event from the system.

Attendee Management:
- Register an Attendee: Associates an attendee with an event.
- List Attendees: Shows attendees for each event.

Speaker & Performer Management:
- Register a Speaker/Performer: Adds a speaker or performer to an event with a description.
- List Speakers/Performers: Displays all registered speakers and performers for an event.
- Edit a Speaker/Performer: Allows editing a speaker’s details.
  If a field is left blank during editing, the original information remains unchanged.

Vendor Management:
- Register a Vendor: Adds a vendor with their products/services.
- List Vendors: Displays all registered vendors for an event.
- Edit a Vendor: Allows editing a vendor’s details.
  If a field is left blank during editing, the original information remains unchanged.

Feedback & Surveys:
- Submit Feedback: Allows attendees to leave feedback for an event.

Budget & Financial Management:
- Update Budget: Increases the event's budget by adding a specified amount.
- View Budget: Retrieves the current budget of an event.
- Edit Budget: Overwrites the event's budget with a new value.
  If no new value is provided during editing, the original budget remains unchanged.

---

## Missing Features

The following features were not implemented due to the need for data persistence:
- Social Media Integration: Promoting events and engaging with attendees on social media platforms.
- Venue Booking: Integration with venue databases for booking and management.
