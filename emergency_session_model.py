from datetime import datetime, timedelta
from config import db


def create_emergency_session(session_data):
    session = {
        "patient_id": session_data["patient_id"],
        "accessed_by": session_data.get("accessed_by"),
        "access_type": session_data.get("access_type", "emergency"),
        "status": "active",
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=30)
    }

    result = db.emergency_sessions.insert_one(session)

    return str(result.inserted_id)


def get_active_emergency_session(session_id):
    from bson import ObjectId

    session = db.emergency_sessions.find_one({
        "_id": ObjectId(session_id),
        "status": "active"
    })

    if not session:
        return None

    if session["expires_at"] <= datetime.utcnow():
        db.emergency_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"status": "expired"}}
        )
        return None

    return session


def end_emergency_session(session_id):
    from bson import ObjectId

    result = db.emergency_sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"status": "ended"}}
    )

    return result.modified_count > 0