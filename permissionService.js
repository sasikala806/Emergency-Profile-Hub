import { apiRequest } from "./api";
import { getToken } from "./authService";

export async function grantPermission(
  grantedToUserId,
  permissionType
) {
  const token = getToken();

  return apiRequest("/permissions/grant", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      granted_to_user_id: grantedToUserId,
      permission_type: permissionType,
    }),
  });
}

export async function checkPermission(
  patientId,
  permissionType
) {
  const token = getToken();

  return apiRequest(
    `/permissions/check?patient_id=${patientId}&permission_type=${permissionType}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
}

export async function revokePermission(permissionId) {
  const token = getToken();

  return apiRequest(`/permissions/revoke/${permissionId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}