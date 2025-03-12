from flask import Flask, request, jsonify
from models.event import Event
from models.participant import Participant
from models.speaker import Speaker
from models.vendor import Vendor
from models.feedback import Feedback
from database.db import SessionLocal
from datetime import datetime

class EventApp:
    def __init__(self):
        self.app = Flask(__name__)
        self._register_routes()

    def _register_routes(self):
        self.app.add_url_rule("/events", "list_events", self.list_events, methods=["GET"])
        self.app.add_url_rule("/create_event", "create_event", self.create_event, methods=["POST"])
        self.app.add_url_rule("/edit_event", "edit_event", self.edit_event, methods=["POST"])
        self.app.add_url_rule("/delete_event", "delete_event", self.delete_event, methods=["POST"])
        self.app.add_url_rule("/update_budget", "update_budget", self.update_budget, methods=["POST"])
        self.app.add_url_rule("/get_budget", "get_budget", self.get_budget, methods=["GET"])
        self.app.add_url_rule("/edit_budget", "edit_budget", self.edit_budget, methods=["POST"])
        self.app.add_url_rule("/register_participant", "register_participant", self.register_participant, methods=["POST"])
        self.app.add_url_rule("/attendees", "get_attendees", self.get_attendees, methods=["GET"])
        self.app.add_url_rule("/edit_participant", "edit_participant", self.edit_participant, methods=["POST"])  # Definido agora
        self.app.add_url_rule("/register_speaker", "register_speaker", self.register_speaker, methods=["POST"])
        self.app.add_url_rule("/list_speakers", "list_speakers", self.list_speakers, methods=["GET"])
        self.app.add_url_rule("/edit_speaker", "edit_speaker", self.edit_speaker, methods=["POST"])
        self.app.add_url_rule("/register_vendor", "register_vendor", self.register_vendor, methods=["POST"])
        self.app.add_url_rule("/list_vendors", "list_vendors", self.list_vendors, methods=["GET"])
        self.app.add_url_rule("/edit_vendor", "edit_vendor", self.edit_vendor, methods=["POST"])
        self.app.add_url_rule("/add_feedback", "add_feedback", self.add_feedback, methods=["POST"])

    def _get_session(self):
        """Helper function to handle database session."""
        return SessionLocal()

    def list_events(self):
        session = self._get_session()
        try:
            events = session.query(Event).all()
            return jsonify([e.to_dict() for e in events])
        finally:
            session.close()

    def create_event(self):
        session = self._get_session()
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON format"}), 400

            name = data.get("name")
            date = data.get("date")
            budget = data.get("budget", 0)

            if not name or not date:
                return jsonify({"error": "Missing required fields"}), 400

            try:
                date = datetime.strptime(date, "%d-%m-%Y").date()
            except ValueError:
                return jsonify({"error": "Date must be in DD-MM-YYYY format"}), 400

            try:
                budget = int(budget)
            except ValueError:
                return jsonify({"error": "Budget must be a valid number"}), 400

            event = Event(name=name, date=date, budget=budget)
            session.add(event)
            session.commit()
            session.refresh(event)
            return jsonify(event.to_dict()), 201
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    def edit_event(self):
        session = self._get_session()
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

    def delete_event(self):
        session = self._get_session()
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

    def update_budget(self):
        session = self._get_session()
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

    def get_budget(self):
        session = self._get_session()
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

    def edit_budget(self):
        session = self._get_session()
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

    def register_participant(self):
        session = self._get_session()
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

    def get_attendees(self):
        session = self._get_session()
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

    def edit_participant(self):
        session = self._get_session()
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

    def register_speaker(self):
        session = self._get_session()
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

    def list_speakers(self):
        session = self._get_session()
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

    def edit_speaker(self):
        session = self._get_session()
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON format"}), 400

            speaker_id = data.get("speaker_id")
            new_name = data.get("new_name")
            new_description = data.get("new_description")

            speaker = session.query(Speaker).filter(Speaker.id == speaker_id).first()
            if not speaker:
                return jsonify({"error": "Speaker not found"}), 404

            if new_name is not None and new_name.strip() != "":
                speaker.name = new_name

            if new_description is not None and new_description.strip() != "":
                speaker.description = new_description

            session.commit()
            return jsonify({"message": "Speaker updated", "speaker": speaker.to_dict()})
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    def register_vendor(self):
        session = self._get_session()
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

    def list_vendors(self):
        session = self._get_session()
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

    def edit_vendor(self):
        session = self._get_session()
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON format"}), 400

            vendor_id = data.get("vendor_id")
            new_name = data.get("new_name")
            new_services = data.get("new_services")

            if not vendor_id:
                return jsonify({"error": "Missing vendor_id"}), 400

            if (new_name is None or new_name.strip() == "") and (new_services is None or new_services.strip() == ""):
                return jsonify({"error": "At least one field (new_name or new_services) must be provided to update"}), 400

            vendor = session.query(Vendor).filter(Vendor.id == vendor_id).first()
            if not vendor:
                return jsonify({"error": "Vendor not found"}), 404

            if new_name is not None and new_name.strip() != "":
                vendor.name = new_name
            if new_services is not None and new_services.strip() != "":
                vendor.services = new_services

            session.commit()
            return jsonify({"message": "Vendor updated", "vendor": vendor.to_dict()})
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    def add_feedback(self):
        session = self._get_session()
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

    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    app = EventApp()
    app.run()
