from flask import Blueprint, request, jsonify

from utils.security import token_required, role_required
from services.permission_service import (
    grant_permission,
    check_permission,
    remove_permission
)


permission_bp = Blueprint("permission", __name__)


@permission_bp.route("/grant", methods=["POST"])
@token_required
@role_required("patient")
def grant():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    required_fields = [
        "granted_to_user_id",
        "permission_type"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400

    try:
        permission_id = grant_permission(
            request.user["user_id"],
            data["granted_to_user_id"],
            data["permission_type"]
        )

        return jsonify({
            "message": "Permission granted successfully",
            "permission_id": permission_id
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Failed to grant permission",
            "error": str(e)
        }), 500


@permission_bp.route("/check", methods=["GET"])
@token_required
def check():
    patient_id = request.args.get("patient_id")
    permission_type = request.args.get("permission_type")

    if not patient_id or not permission_type:
        return jsonify({
            "message": "patient_id and permission_type are required"
        }), 400

    granted_to_user_id = request.user["user_id"]

    has_permission = check_permission(
        patient_id,
        granted_to_user_id,
        permission_type
    )

    return jsonify({
        "has_permission": has_permission
    }), 200


@permission_bp.route("/revoke/<permission_id>", methods=["DELETE"])
@token_required
@role_required("patient")
def revoke(permission_id):
    try:
        removed = remove_permission(permission_id, request.user["user_id"])
        
        if not removed:
            return jsonify({
                "message": "Permission not found"
            }), 404

        return jsonify({
            "message": "Permission revoked successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Failed to revoke permission",
            "error": str(e)
        }), 500