# controllers/speaker_controller.py
from flask import Blueprint, request, jsonify
from services.speaker_service import SpeakerService

bp = Blueprint("speaker", __name__)
speaker_service = SpeakerService()

@bp.route("/register_speaker", methods=["POST"])
def register_speaker():
    data = request.get_json()
    event_id = data.get("event_id")
    name = data.get("name")
    description = data.get("description")
    if not event_id or not name:
        return jsonify({"error": "Missing event_id or speaker name"}), 400
    speaker = speaker_service.register_speaker(event_id, name, description)
    if not speaker:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Speaker registered", "speaker": speaker})

@bp.route("/list_speakers", methods=["GET"])
def list_speakers():
    event_id = request.args.get("event_id")
    speakers = speaker_service.list_speakers(event_id)
    if speakers is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"speakers": speakers})

@bp.route("/edit_speaker", methods=["POST"])
def edit_speaker():
    data = request.get_json()
    speaker = speaker_service.edit_speaker(
        data.get("speaker_id"), data.get("new_name"), data.get("new_description")
    )
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404
    return jsonify({"message": "Speaker updated", "speaker": speaker})
