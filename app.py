from flask import Flask, request, jsonify
from models.event import Event
from database.db import SessionLocal

# Import dos novos modelos
from models.participant import Participant
from models.speaker import Speaker
from models.vendor import Vendor
from models.feedback import Feedback

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

# Endpoints para PARTICIPANTES

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

        participant = Participant(name=name, event_id=event_id)
        session.add(participant)
        session.commit()
        session.refresh(participant)
        return jsonify({"message": "Participant registered", "participant": participant.to_dict()})
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
        return jsonify({"participants": [p.to_dict() for p in event.participants]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Novo endpoint para EDITAR PARTICIPANTE

@app.route("/edit_participant", methods=["POST"])
def edit_participant():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        participant_id = data.get("participant_id")
        new_name = data.get("new_name")
        if not participant_id or not new_name:
            return jsonify({"error": "Missing participant_id or new_name"}), 400

        participant = session.query(Participant).filter(Participant.id == participant_id).first()
        if not participant:
            return jsonify({"error": "Participant not found"}), 404

        participant.name = new_name
        session.commit()
        return jsonify({"message": "Participant updated", "participant": participant.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Endpoints para PALESTRANTES

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

        speaker = Speaker(name=name, description=description, event_id=event_id)
        session.add(speaker)
        session.commit()
        session.refresh(speaker)
        return jsonify({"message": "Speaker registered", "speaker": speaker.to_dict()})
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
        return jsonify({"speakers": [s.to_dict() for s in event.speakers]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Endpoint para EDITAR PALESTRANTE (opção 9 corrigida)
@app.route("/edit_speaker", methods=["POST"])
def edit_speaker():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        speaker_id = data.get("speaker_id")
        if not speaker_id:
            return jsonify({"error": "Missing speaker_id"}), 400

        new_name = data.get("new_name")
        new_description = data.get("new_description")

        speaker = session.query(Speaker).filter(Speaker.id == speaker_id).first()
        if not speaker:
            return jsonify({"error": "Speaker not found"}), 404

        # Atualiza o nome se for fornecido e não for vazio
        if new_name is not None and new_name.strip() != "":
            speaker.name = new_name

        # Atualiza a descrição se for fornecida e não for vazia
        if new_description is not None and new_description.strip() != "":
            speaker.description = new_description

        session.commit()
        return jsonify({"message": "Speaker updated", "speaker": speaker.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Endpoints para FORNECEDORES

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

        vendor = Vendor(name=name, services=services, event_id=event_id)
        session.add(vendor)
        session.commit()
        session.refresh(vendor)
        return jsonify({"message": "Vendor registered", "vendor": vendor.to_dict()})
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
        return jsonify({"vendors": [v.to_dict() for v in event.vendors]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Endpoint para EDITAR FORNECEDOR (opção 12 corrigida)

@app.route("/edit_vendor", methods=["POST"])
def edit_vendor():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        vendor_id = data.get("vendor_id")
        new_name = data.get("new_name")
        new_services = data.get("new_services")
        
        if not vendor_id:
            return jsonify({"error": "Missing vendor_id"}), 400

        # Verifica se pelo menos um dos campos foi fornecido para atualizar
        if (new_name is None or new_name.strip() == "") and (new_services is None or new_services.strip() == ""):
            return jsonify({"error": "At least one field (new_name or new_services) must be provided to update"}), 400

        vendor = session.query(Vendor).filter(Vendor.id == vendor_id).first()
        if not vendor:
            return jsonify({"error": "Vendor not found"}), 404

        # Atualiza o nome se for fornecido e não for vazio
        if new_name is not None and new_name.strip() != "":
            vendor.name = new_name
        # Atualiza os serviços se for fornecido e não for vazio
        if new_services is not None and new_services.strip() != "":
            vendor.services = new_services

        session.commit()
        return jsonify({"message": "Vendor updated", "vendor": vendor.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Endpoints para FEEDBACK

@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        event_id = data.get("event_id")
        content = data.get("feedback")
        if not event_id or not content:
            return jsonify({"error": "Missing event_id or feedback"}), 400

        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        feedback = Feedback(content=content, event_id=event_id)
        session.add(feedback)
        session.commit()
        session.refresh(feedback)
        return jsonify({"message": "Feedback added", "feedback": feedback.to_dict()})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
