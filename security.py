import jwt
from functools import wraps
from flask import request, jsonify
from config import JWT_SECRET


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "Authorization token is required"
            }), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "message": "Invalid authorization format"
            }), 401

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=["HS256"]
            )

            request.user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({
                "message": "Token has expired"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "message": "Invalid token"
            }), 401

        return f(*args, **kwargs)

    return decorated
def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(request, "user", None)

            if not user:
                return jsonify({
                    "message": "Authentication required"
                }), 401

            user_role = user.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "message": "Access denied"
                }), 403

            return f(*args, **kwargs)

        return decorated
    return decorator