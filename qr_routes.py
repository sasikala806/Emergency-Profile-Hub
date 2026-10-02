from flask import Blueprint, request, jsonify, send_file

from utils.security import token_required
from services.qr_service import (
    create_patient_qr,
    get_patient_from_qr,
    disable_patient_qr,
    start_emergency_access,
    get_emergency_session,
    end_emergency_access
)


qr_bp = Blueprint("qr", __name__)


@qr_bp.route("/generate", methods=["POST"])
@token_required
def generate_qr():
    patient_id = request.user["user_id"]

    try:
        qr_token = create_patient_qr(patient_id)

        return jsonify({
    "message": "QR generated successfully",
    "qr_token": qr_token,
    "qr_image": f"/api/qr/image/{patient_id}"
}), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to generate QR",
            "error": str(e)
        }), 500
@qr_bp.route("/image/<patient_id>", methods=["GET"])
def qr_image(patient_id):
    import os

    qr_file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "qr_images",
        f"{patient_id}.png"
    )

    if not os.path.exists(qr_file_path):
        return jsonify({
            "message": "QR image not found"
        }), 404

    return send_file(
        qr_file_path,
        mimetype="image/png"
    )

@qr_bp.route("/verify/<qr_token>", methods=["GET"])
def verify_qr(qr_token):
    try:
        patient_id = get_patient_from_qr(qr_token)

        if not patient_id:
            return jsonify({
                "message": "Invalid or inactive QR"
            }), 404

        return jsonify({
            "message": "QR verified successfully",
            "patient_id": patient_id
        }), 200

    except Exception as e:
        return jsonify({
            "message": "QR verification failed",
            "error": str(e)
        }), 500

@qr_bp.route("/disable/<qr_token>", methods=["POST"])
@token_required
def disable_qr(qr_token):
    from models.qr_model import get_qr_by_token

    qr = get_qr_by_token(qr_token)

    if not qr:
        return jsonify({
            "message": "QR not found or already inactive"
        }), 404

    if qr["patient_id"] != request.user["user_id"]:
        return jsonify({
            "message": "You can only disable your own QR"
        }), 403

    try:
        disabled = disable_patient_qr(qr_token)

        if not disabled:
            return jsonify({
                "message": "Failed to disable QR"
            }), 500

        return jsonify({
            "message": "QR disabled successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to disable QR",
            "error": str(e)
        }), 500

@qr_bp.route("/emergency/start/<qr_token>", methods=["POST"])
def start_emergency(qr_token):
    try:
        patient_id = get_patient_from_qr(qr_token)

        if not patient_id:
            return jsonify({
                "message": "Invalid or inactive QR"
            }), 404

        session_id = start_emergency_access(
            patient_id=patient_id,
            accessed_by=None
        )

        return jsonify({
            "message": "Emergency access session started",
            "session_id": session_id,
            "patient_id": patient_id
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Failed to start emergency access",
            "error": str(e)
        }), 500


@qr_bp.route("/emergency/session/<session_id>", methods=["GET"])
def emergency_session(session_id):
    try:
        session = get_emergency_session(session_id)

        if not session:
            return jsonify({
                "message": "Emergency session is invalid or expired"
            }), 404

        return jsonify({
            "message": "Emergency session is active",
            "session_id": session_id,
            "patient_id": session["patient_id"],
            "access_type": session["access_type"],
            "status": session["status"],
            "expires_at": session["expires_at"].isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to retrieve emergency session",
            "error": str(e)
        }), 500


@qr_bp.route("/emergency/end/<session_id>", methods=["POST"])
def end_emergency(session_id):
    try:
        ended = end_emergency_access(session_id)

        if not ended:
            return jsonify({
                "message": "Emergency session not found"
            }), 404

        return jsonify({
            "message": "Emergency access session ended"
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to end emergency session",
            "error": str(e)
        }), 500