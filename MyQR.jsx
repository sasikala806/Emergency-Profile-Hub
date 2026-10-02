import { useState } from "react";
import { generateQR, disableQR } from "../services/qrService";

function MyQR() {
  const [qrToken, setQrToken] = useState("");
  const [qrImage, setQrImage] = useState("");
  const [message, setMessage] = useState("");

  async function handleGenerateQR() {
    try {
      setMessage("");

      const data = await generateQR();

      setQrToken(data.qr_token);
      setQrImage(
        `http://127.0.0.1:5000${data.qr_image}`
      );

      setMessage("QR generated successfully.");
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function handleDisableQR() {
    if (!qrToken) {
      setMessage("Generate a QR first.");
      return;
    }

    try {
      const data = await disableQR(qrToken);

      setMessage(data.message);

      setQrToken("");
      setQrImage("");
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <h1>My Emergency QR</h1>

      <button onClick={handleGenerateQR}>
        Generate QR
      </button>

      {" "}

      <button onClick={handleDisableQR}>
        Disable QR
      </button>

      {message && <p>{message}</p>}

      {qrImage && (
        <div>
          <h3>My QR Code</h3>

          <img
            src={qrImage}
            alt="Emergency QR Code"
            width="250"
          />
        </div>
      )}
    </div>
  );
}

export default MyQR;