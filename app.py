from flask import Flask, request, jsonify
from models.event import Event
from database.db import SessionLocal

app = Flask(__name__)

@app.route("/events", methods=["GET"])
def list_events():
    session = SessionLocal()
    try:
        events = session.query(Event).all()
        return jsonify([e.to_dict() for e in events])
    finally:
        session.close()

@app.route("/create_event", methods=["POST"])
def create_event():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        name = data.get("name")
        date = data.get("date")
        budget = data.get("budget", 0)

        if not name or not date:
            return jsonify({"error": "Missing required fields"}), 400

        event = Event(name=name, date=date, budget=int(budget))
        session.add(event)
        session.commit()
        session.refresh(event)
        return jsonify(event.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/edit_event", methods=["POST"])
def edit_event():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        if "name" in data:
            event.name = data["name"]
        if "date" in data:
            event.date = data["date"]
        if "budget" in data:
            event.budget = int(data["budget"])

        session.commit()
        return jsonify(event.to_dict())
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/delete_event", methods=["POST"])
def delete_event():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        session.delete(event)
        session.commit()
        return jsonify({"message": "Event deleted", "id": event_id})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/update_budget", methods=["POST"])
def update_budget():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        amount = int(data.get("amount", 0))
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        event.budget += amount
        session.commit()
        return jsonify({"message": "Budget updated", "event": event.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/get_budget", methods=["GET"])
def get_budget():
    session = SessionLocal()
    try:
        event_id = request.args.get("event_id")
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify({"budget": event.budget})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/edit_budget", methods=["POST"])
def edit_budget():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        new_budget = int(data.get("new_budget", 0))
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        event.budget = new_budget
        session.commit()
        return jsonify({"message": "Budget updated", "event": event.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/register_participant", methods=["POST"])
def register_participant():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        name = data.get("name")
        if not event_id or not name:
            return jsonify({"error": "Missing event_id or name"}), 400

        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        # Armazenando participantes como uma string separada por vírgulas
        event.participants = f"{event.participants}, {name}" if event.participants else name

        session.commit()
        return jsonify({"message": "Participant registered", "event": event.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/attendees", methods=["GET"])
def get_attendees():
    session = SessionLocal()
    try:
        event_id = request.args.get("event_id")
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify({"participants": event.participants})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/register_speaker", methods=["POST"])
def register_speaker():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        name = data.get("name")
        description = data.get("description")
        if not event_id or not name:
            return jsonify({"error": "Missing event_id or speaker name"}), 400

        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        new_speaker = f"{name} ({description})" if description else name
        event.speakers = f"{event.speakers}, {new_speaker}" if event.speakers else new_speaker

        session.commit()
        return jsonify({"message": "Speaker registered", "event": event.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/list_speakers", methods=["GET"])
def list_speakers():
    session = SessionLocal()
    try:
        event_id = request.args.get("event_id")
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify({"speakers": event.speakers})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/edit_speaker", methods=["POST"])
def edit_speaker():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        old_name = data.get("old_name")
        new_name = data.get("new_name")
        new_description = data.get("new_description")
        if not event_id or not old_name or not new_name:
            return jsonify({"error": "Missing parameters"}), 400

        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        speakers = event.speakers.split(", ") if event.speakers else []
        updated = False
        for i, sp in enumerate(speakers):
            if sp.startswith(old_name):
                speakers[i] = f"{new_name} ({new_description})" if new_description else new_name
                updated = True
        if not updated:
            return jsonify({"error": "Speaker not found"}), 404

        event.speakers = ", ".join(speakers)
        session.commit()
        return jsonify({"message": "Speaker updated", "event": event.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/register_vendor", methods=["POST"])
def register_vendor():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        name = data.get("name")
        services = data.get("services")
        if not event_id or not name:
            return jsonify({"error": "Missing event_id or vendor name"}), 400

        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        new_vendor = f"{name} ({services})" if services else name
        event.vendors = f"{event.vendors}, {new_vendor}" if event.vendors else new_vendor

        session.commit()
        return jsonify({"message": "Vendor registered", "event": event.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/list_vendors", methods=["GET"])
def list_vendors():
    session = SessionLocal()
    try:
        event_id = request.args.get("event_id")
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify({"vendors": event.vendors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/edit_vendor", methods=["POST"])
def edit_vendor():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        old_name = data.get("old_name")
        new_name = data.get("new_name")
        new_services = data.get("new_services")
        if not event_id or not old_name or not new_name:
            return jsonify({"error": "Missing parameters"}), 400

        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        vendors = event.vendors.split(", ") if event.vendors else []
        updated = False
        for i, ven in enumerate(vendors):
            if ven.startswith(old_name):
                vendors[i] = f"{new_name} ({new_services})" if new_services else new_name
                updated = True
        if not updated:
            return jsonify({"error": "Vendor not found"}), 404

        event.vendors = ", ".join(vendors)
        session.commit()
        return jsonify({"message": "Vendor updated", "event": event.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        feedback = data.get("feedback")
        if not event_id or not feedback:
            return jsonify({"error": "Missing event_id or feedback"}), 400

        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        event.feedback = f"{event.feedback}\n{feedback}" if event.feedback else feedback

        session.commit()
        return jsonify({"message": "Feedback added", "event": event.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
