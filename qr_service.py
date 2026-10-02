import secrets
import os
from utils.qr_generator import generate_qr_image
from models.qr_model import (
    create_qr,
    get_qr_by_token,
    get_qr_by_patient,
    deactivate_qr
)
from models.emergency_session_model import (
    create_emergency_session,
    get_active_emergency_session,
    end_emergency_session
)

def generate_qr_token():
    return secrets.token_urlsafe(32)


def create_patient_qr(patient_id):
    qr_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "qr_images"
    )

    os.makedirs(qr_folder, exist_ok=True)

    qr_file_path = os.path.join(
        qr_folder,
        f"{patient_id}.png"
    )

    existing_qr = get_qr_by_patient(patient_id)

    if existing_qr:
        if not os.path.exists(qr_file_path):
            generate_qr_image(
                existing_qr["qr_token"],
                qr_file_path
            )

        return existing_qr["qr_token"]

    qr_token = generate_qr_token()

    qr_data = {
        "patient_id": patient_id,
        "qr_token": qr_token
    }

    create_qr(qr_data)

    generate_qr_image(
        qr_token,
        qr_file_path
    )

    return qr_token
def get_patient_from_qr(qr_token):
    qr = get_qr_by_token(qr_token)

    if not qr:
        return None

    return qr["patient_id"]


def disable_patient_qr(qr_token):
    return deactivate_qr(qr_token)
def start_emergency_access(patient_id, accessed_by=None):
    session_data = {
        "patient_id": patient_id,
        "accessed_by": accessed_by,
        "access_type": "emergency"
    }

    return create_emergency_session(session_data)


def get_emergency_session(session_id):
    return get_active_emergency_session(session_id)


def end_emergency_access(session_id):
    return end_emergency_session(session_id)