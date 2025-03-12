# controllers/vendor_controller.py
from flask import Blueprint, request, jsonify
from services.vendor_service import VendorService

bp = Blueprint("vendor", __name__)
vendor_service = VendorService()

@bp.route("/register_vendor", methods=["POST"])
def register_vendor():
    data = request.get_json()
    event_id = data.get("event_id")
    name = data.get("name")
    services_offered = data.get("services")
    if not event_id or not name:
        return jsonify({"error": "Missing event_id or vendor name"}), 400
    vendor = vendor_service.register_vendor(event_id, name, services_offered)
    if not vendor:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Vendor registered", "vendor": vendor})

@bp.route("/list_vendors", methods=["GET"])
def list_vendors():
    event_id = request.args.get("event_id")
    vendors = vendor_service.list_vendors(event_id)
    if vendors is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"vendors": vendors})

@bp.route("/edit_vendor", methods=["POST"])
def edit_vendor():
    data = request.get_json()
    vendor = vendor_service.edit_vendor(
        data.get("vendor_id"), data.get("new_name"), data.get("new_services")
    )
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404
    return jsonify({"message": "Vendor updated", "vendor": vendor})
