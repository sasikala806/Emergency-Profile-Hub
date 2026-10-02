from datetime import datetime
from werkzeug.security import generate_password_hash
from config import db


def create_user(user_data):
    existing_user = db.users.find_one({
        "email": user_data["email"]
    })

    if existing_user:
        return None

    user = {
        "name": user_data["name"],
        "email": user_data["email"],
        "password": generate_password_hash(user_data["password"]),
        "role": user_data.get("role", "patient"),
        "created_at": datetime.utcnow()
    }

    result = db.users.insert_one(user)

    return str(result.inserted_id)