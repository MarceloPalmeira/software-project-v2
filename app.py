from flask import Flask, request, jsonify
from event_mng import EventMng
from participants_mng import ParticipantsMng
from speakers_mng import SpeakersMng
from vendors_mng import VendorsMng
from budget_financial_mng import BudgetandFinancialMng

app = Flask(__name__)

event_manager = EventMng()
participants_manager = ParticipantsMng()
speakers_manager = SpeakersMng()
vendors_manager = VendorsMng()
budget_manager = BudgetandFinancialMng()

def get_event_or_404(event_id):
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return None, jsonify({"error": "Event not found"}), 404
    return event, None, None

@app.route("/", methods=["GET"])
def list_events():
    return jsonify(event_manager.list_events())

@app.route("/create_event", methods=["POST"])
def create_event():
    name = request.form.get("name")
    date = request.form.get("date")
    budget = request.form.get("budget", "0")
    try:
        budget = int(budget)
    except ValueError:
        budget = 0
    return jsonify(event_manager.create_event(name, date, budget))

@app.route("/edit_event", methods=["POST"])
def edit_event():
    event_id = int(request.form.get("event_id"))
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    new_name = request.form.get("name")
    new_date = request.form.get("date")
    new_budget_str = request.form.get("budget", "")
    
    if new_name == "":
        new_name = event.name
    if new_date == "":
        new_date = event.date
    if new_budget_str == "":
        new_budget = event.budget
    else:
        try:
            new_budget = int(new_budget_str)
        except ValueError:
            new_budget = event.budget

    updated_event = event_manager.edit_event(event_id, new_name, new_date, new_budget)
    return jsonify(updated_event)

@app.route("/delete_event", methods=["POST"])
def delete_event():
    event_id = int(request.form.get("event_id"))
    result = event_manager.remove_event(event_id)
    return jsonify(result)

@app.route("/register_participant", methods=["POST"])
def register_participant():
    name = request.form.get("name")
    event_id = int(request.form.get("event_id"))
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    participants_manager.register_participant(event, name)
    return jsonify({"message": "Participant successfully registered", "event": event.to_dict()})

@app.route("/attendees", methods=["GET"])
def list_attendees():
    attendees = {event.id: event.attendees for event in event_manager.events}
    return jsonify(attendees)

@app.route("/register_speaker", methods=["POST"])
def register_speaker():
    name = request.form.get("name")
    description = request.form.get("description")
    event_id = int(request.form.get("event_id"))
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    speakers_manager.register_speaker(event, name, description)
    return jsonify({"message": "Speaker successfully registered", "event": event.to_dict()})

@app.route("/list_speakers", methods=["GET"])
def list_speakers():
    event_id = int(request.args.get("event_id"))
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    speakers = speakers_manager.list_speakers(event)
    return jsonify({"speakers": speakers})

@app.route("/edit_speaker", methods=["POST"])
def edit_speaker():
    event_id = int(request.form.get("event_id"))
    old_name = request.form.get("old_name")
    new_name = request.form.get("new_name")
    new_description = request.form.get("new_description")
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    current_speaker = None
    for sp in event.speakers:
        if sp["name"] == old_name:
            current_speaker = sp
            break
    if not current_speaker:
        return jsonify({"error": "Speaker not found"}), 404
    if new_name == "":
        new_name = current_speaker["name"]
    if new_description == "":
        new_description = current_speaker["description"]
    if speakers_manager.edit_speaker(event, old_name, new_name, new_description):
        return jsonify({"message": "Speaker updated successfully", "event": event.to_dict()})
    return jsonify({"error": "Speaker not found"}), 404

@app.route("/register_vendor", methods=["POST"])
def register_vendor():
    name = request.form.get("name")
    services = request.form.get("services")
    event_id = int(request.form.get("event_id"))
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    vendors_manager.register_vendor(event, name, services)
    return jsonify({"message": "Vendor successfully registered", "event": event.to_dict()})

@app.route("/list_vendors", methods=["GET"])
def list_vendors():
    event_id = int(request.args.get("event_id"))
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    vendors = vendors_manager.list_vendors(event)
    return jsonify({"vendors": vendors})

@app.route("/edit_vendor", methods=["POST"])
def edit_vendor():
    event_id = int(request.form.get("event_id"))
    old_name = request.form.get("old_name")
    new_name = request.form.get("new_name")
    new_services = request.form.get("new_services")
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    current_vendor = None
    for v in event.vendors:
        if v["name"] == old_name:
            current_vendor = v
            break
    if not current_vendor:
        return jsonify({"error": "Vendor not found"}), 404
    if new_name == "":
        new_name = current_vendor["name"]
    if new_services == "":
        new_services = current_vendor["services"]
    if vendors_manager.edit_vendor(event, old_name, new_name, new_services):
        return jsonify({"message": "Vendor updated successfully", "event": event.to_dict()})
    return jsonify({"error": "Vendor not found"}), 404

@app.route("/update_budget", methods=["POST"])
def update_budget():
    event_id = int(request.form.get("event_id"))
    amount_str = request.form.get("amount", "")
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    try:
        amount = int(amount_str)
    except ValueError:
        amount = 0
    budget_manager.update_budget(event, amount)
    return jsonify({"message": "Budget successfully updated", "event": event.to_dict()})

@app.route("/get_budget", methods=["GET"])
def get_budget():
    event_id = int(request.args.get("event_id"))
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    budget = budget_manager.get_budget(event)
    return jsonify({"budget": budget})

@app.route("/edit_budget", methods=["POST"])
def edit_budget():
    event_id = int(request.form.get("event_id"))
    new_budget_str = request.form.get("new_budget", "")
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    if new_budget_str == "":
        new_budget = event.budget
    else:
        try:
            new_budget = int(new_budget_str)
        except ValueError:
            new_budget = event.budget
    budget_manager.set_budget(event, new_budget)
    return jsonify({"message": "Budget updated successfully", "event": event.to_dict()})

@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    event_id = int(request.form.get("event_id"))
    feedback = request.form.get("feedback")
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    event_manager.add_feedback(event_id, feedback)
    return jsonify({"message": "Feedback successfully added", "event": event.to_dict()})

if __name__ == "__main__":
    app.run(debug=True)
