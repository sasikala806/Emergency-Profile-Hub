from datetime import datetime
from config import db


def create_permission(permission_data):
    permission = {
        "patient_id": permission_data["patient_id"],
        "granted_to_user_id": permission_data["granted_to_user_id"],
        "permission_type": permission_data["permission_type"],
        "status": permission_data.get("status", "active"),
        "created_at": datetime.utcnow()
    }

    result = db.permissions.insert_one(permission)

    return str(result.inserted_id)


def get_permission(patient_id, granted_to_user_id, permission_type):
    return db.permissions.find_one({
        "patient_id": patient_id,
        "granted_to_user_id": granted_to_user_id,
        "permission_type": permission_type,
        "status": "active"
    })


def revoke_permission(permission_id, patient_id):
    from bson import ObjectId

    result = db.permissions.update_one(
        {
            "_id": ObjectId(permission_id),
            "patient_id": patient_id,
            "status": "active"
        },
        {
            "$set": {
                "status": "revoked"
            }
        }
    )

    return result.modified_count > 0