from datetime import datetime
from config import db


def create_qr(qr_data):
    qr_record = {
        "patient_id": qr_data["patient_id"],
        "qr_token": qr_data["qr_token"],
        "status": "active",
        "created_at": datetime.utcnow()
    }

    result = db.qr_codes.insert_one(qr_record)

    return str(result.inserted_id)


def get_qr_by_token(qr_token):
    return db.qr_codes.find_one({
        "qr_token": qr_token,
        "status": "active"
    })


def get_qr_by_patient(patient_id):
    return db.qr_codes.find_one({
        "patient_id": patient_id,
        "status": "active"
    })


def deactivate_qr(qr_token):
    result = db.qr_codes.update_one(
        {"qr_token": qr_token},
        {"$set": {"status": "inactive"}}
    )

    return result.modified_count > 0