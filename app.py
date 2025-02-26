from flask import Flask, request, jsonify
from models.event import Event

app = Flask(__name__)

# In-memory storage for events
events = []
next_event_id = 1

def get_event_by_id(event_id):
    for e in events:
        if e.id == event_id:
            return e
    return None

@app.route("/", methods=["GET"])
def list_events():
    return jsonify([e.to_dict() for e in events])

@app.route("/create_event", methods=["POST"])
def create_event():
    global next_event_id
    name = request.form.get("name")
    date = request.form.get("date")
    budget = request.form.get("budget", "0")
    try:
        budget = int(budget)
    except ValueError:
        budget = 0
    event = Event(next_event_id, name, date, budget)
    events.append(event)
    next_event_id += 1
    return jsonify(event.to_dict())

@app.route("/edit_event", methods=["POST"])
def edit_event():
    event_id = int(request.form.get("event_id"))
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    new_name = request.form.get("name")
    new_date = request.form.get("date")
    new_budget_str = request.form.get("budget", "")
    
    if new_name:
        event.name = new_name
    if new_date:
        event.date = new_date
    if new_budget_str:
        try:
            event.budget = int(new_budget_str)
        except ValueError:
            pass
    return jsonify(event.to_dict())

@app.route("/delete_event", methods=["POST"])
def delete_event():
    event_id = int(request.form.get("event_id"))
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    events.remove(event)
    return jsonify({"message": "Event deleted", "id": event_id})

@app.route("/register_participant", methods=["POST"])
def register_participant():
    name = request.form.get("name")
    event_id = int(request.form.get("event_id"))
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    event.attendees.append(name)
    return jsonify({"message": "Participant registered", "event": event.to_dict()})

@app.route("/attendees", methods=["GET"])
def list_attendees():
    return jsonify({e.id: e.attendees for e in events})

@app.route("/register_speaker", methods=["POST"])
def register_speaker():
    name = request.form.get("name")
    description = request.form.get("description")
    event_id = int(request.form.get("event_id"))
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    event.speakers.append({"name": name, "description": description})
    return jsonify({"message": "Speaker registered", "event": event.to_dict()})

@app.route("/list_speakers", methods=["GET"])
def list_speakers():
    event_id = int(request.args.get("event_id"))
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"speakers": event.speakers})

@app.route("/edit_speaker", methods=["POST"])
def edit_speaker():
    event_id = int(request.form.get("event_id"))
    old_name = request.form.get("old_name")
    new_name = request.form.get("new_name")
    new_description = request.form.get("new_description")
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    speaker = None
    for sp in event.speakers:
        if sp["name"] == old_name:
            speaker = sp
            break
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404
    if new_name:
        speaker["name"] = new_name
    if new_description:
        speaker["description"] = new_description
    return jsonify({"message": "Speaker updated", "event": event.to_dict()})

@app.route("/register_vendor", methods=["POST"])
def register_vendor():
    name = request.form.get("name")
    services = request.form.get("services")
    event_id = int(request.form.get("event_id"))
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    event.vendors.append({"name": name, "services": services})
    return jsonify({"message": "Vendor registered", "event": event.to_dict()})

@app.route("/list_vendors", methods=["GET"])
def list_vendors():
    event_id = int(request.args.get("event_id"))
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"vendors": event.vendors})

@app.route("/edit_vendor", methods=["POST"])
def edit_vendor():
    event_id = int(request.form.get("event_id"))
    old_name = request.form.get("old_name")
    new_name = request.form.get("new_name")
    new_services = request.form.get("new_services")
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    vendor = None
    for v in event.vendors:
        if v["name"] == old_name:
            vendor = v
            break
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404
    if new_name:
        vendor["name"] = new_name
    if new_services:
        vendor["services"] = new_services
    return jsonify({"message": "Vendor updated", "event": event.to_dict()})

@app.route("/update_budget", methods=["POST"])
def update_budget():
    event_id = int(request.form.get("event_id"))
    amount_str = request.form.get("amount", "")
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    try:
        amount = int(amount_str)
    except ValueError:
        amount = 0
    event.budget += amount
    return jsonify({"message": "Budget updated", "event": event.to_dict()})

@app.route("/get_budget", methods=["GET"])
def get_budget():
    event_id = int(request.args.get("event_id"))
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"budget": event.budget})

@app.route("/edit_budget", methods=["POST"])
def edit_budget():
    event_id = int(request.form.get("event_id"))
    new_budget_str = request.form.get("new_budget", "")
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    if new_budget_str:
        try:
            event.budget = int(new_budget_str)
        except ValueError:
            pass
    return jsonify({"message": "Budget updated", "event": event.to_dict()})

@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    event_id = int(request.form.get("event_id"))
    feedback = request.form.get("feedback")
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    event.feedbacks.append(feedback)
    return jsonify({"message": "Feedback added", "event": event.to_dict()})

if __name__ == "__main__":
    app.run(debug=True)
