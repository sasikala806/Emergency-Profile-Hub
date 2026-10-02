import { apiRequest } from "./api";
import { getToken } from "./authService";

export async function generateQR() {
  const token = getToken();

  return apiRequest("/qr/generate", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function verifyQR(qrToken) {
  return apiRequest(`/qr/verify/${qrToken}`, {
    method: "GET",
  });
}

export async function disableQR(qrToken) {
  const token = getToken();

  return apiRequest(`/qr/disable/${qrToken}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function getQRImageUrl(patientId) {
  return `http://127.0.0.1:5000/api/qr/image/${patientId}`;
}