# controllers/participant_controller.py
from flask import Blueprint, request, jsonify
from services.participant_service import ParticipantService

bp = Blueprint("participant", __name__)
participant_service = ParticipantService()

@bp.route("/register_participant", methods=["POST"])
def register_participant():
    data = request.get_json()
    event_id = data.get("event_id")
    name = data.get("name")
    if not event_id or not name:
        return jsonify({"error": "Missing event_id or name"}), 400
    participant = participant_service.register_participant(event_id, name)
    if not participant:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Participant registered", "participant": participant})

@bp.route("/attendees", methods=["GET"])
def get_attendees():
    event_id = request.args.get("event_id")
    attendees = participant_service.get_attendees(event_id)
    if attendees is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"participants": attendees})

@bp.route("/edit_participant", methods=["POST"])
def edit_participant():
    data = request.get_json()
    participant = participant_service.edit_participant(data.get("participant_id"), data.get("new_name"))
    if not participant:
        return jsonify({"error": "Participant not found"}), 404
    return jsonify({"message": "Participant updated", "participant": participant})
