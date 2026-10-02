from flask import Blueprint, request, jsonify
from models.user_model import create_user
from config import db, JWT_SECRET
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from utils.security import token_required, role_required



auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body is required"}), 400

    required_fields = ["name", "email", "password"]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field} is required"}), 400

    try:
        user_id = create_user(data)

        if user_id is None:
            return jsonify({
                "message": "Email already registered"
            }), 409

        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id
        }), 201

    except Exception as e:
        return jsonify({
            "message": "User registration failed",
            "error": str(e)
        }), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body is required"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = db.users.find_one({"email": email})

    if not user:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    if not check_password_hash(user["password"], password):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    token_payload = {
        "user_id": str(user["_id"]),
        "email": user["email"],
        "role": user.get("role", "patient"),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(
        token_payload,
        JWT_SECRET,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200

@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user():
    return jsonify({
        "message": "Authenticated user",
        "user": request.user
    }), 200
@auth_bp.route("/patient-only", methods=["GET"])
@token_required
@role_required("patient")
def patient_only():
    return jsonify({
        "message": "Patient role access granted"
    }), 200