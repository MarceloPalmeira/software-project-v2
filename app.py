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

@app.route("/", methods=["GET"])
def list_events():
    return jsonify(event_manager.list_events())

@app.route("/create_event", methods=["POST"])
def create_event():
    name = request.form.get("name")
    date = request.form.get("date")
    budget = request.form.get("budget", 0)
    return jsonify(event_manager.create_event(name, date, int(budget)))

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

@app.route("/update_budget", methods=["POST"])
def update_budget():
    event_id = int(request.form.get("event_id"))
    amount = int(request.form.get("amount"))
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    budget_manager.update_budget(event, amount)
    return jsonify({"message": "Budget successfully updated", "event": event.to_dict()})

@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    event_id = int(request.form.get("event_id"))
    feedback = request.form.get("feedback")
    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    event_manager.add_feedback(event_id, feedback)
    return jsonify({"message": "Feedback successfully added", "event": event.to_dict()})

@app.route("/edit_event", methods=["POST"])
def edit_event():
    event_id = int(request.form.get("event_id"))
    new_name = request.form.get("name")
    new_date = request.form.get("date")
    new_budget = request.form.get("budget", 0)

    event = event_manager.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    updated_event = event_manager.edit_event(event_id, new_name, new_date, int(new_budget))
    return jsonify(updated_event)

@app.route("/delete_event", methods=["POST"])
def delete_event():
    event_id = int(request.form.get("event_id"))
    result = event_manager.remove_event(event_id)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
