from models.permission_model import (
    create_permission,
    get_permission,
    revoke_permission
)


def grant_permission(
    patient_id,
    granted_to_user_id,
    permission_type
):
    permission_data = {
        "patient_id": patient_id,
        "granted_to_user_id": granted_to_user_id,
        "permission_type": permission_type,
        "status": "active"
    }

    return create_permission(permission_data)


def check_permission(
    patient_id,
    granted_to_user_id,
    permission_type
):
    permission = get_permission(
        patient_id,
        granted_to_user_id,
        permission_type
    )

    return permission is not None

def remove_permission(permission_id, patient_id):
    return revoke_permission(
        permission_id,
        patient_id
    )
