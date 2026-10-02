function QRCodeDisplay({ imageUrl }) {
  if (!imageUrl) {
    return <p>No QR code available.</p>;
  }

  return (
    <div>
      <h3>Emergency QR Code</h3>

      <img
        src={imageUrl}
        alt="Emergency QR Code"
        width="250"
      />
    </div>
  );
}

export default QRCodeDisplay;