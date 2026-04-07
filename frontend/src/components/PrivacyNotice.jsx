function PrivacyNotice() {
  return (
    <div
      style={{
        marginTop: "16px",
        padding: "12px",
        border: "1px solid #ccc",
        borderRadius: "6px",
        fontSize: "14px",
        backgroundColor: "#f9f9f9",
      }}
    >
      <strong>Privacy notice</strong>
      <ul style={{ marginTop: "8px", paddingLeft: "20px" }}>
        <li>The PDF file stays on your device and is not uploaded.</li>
        <li>Only extracted text is sent for analysis.</li>
        <li>We do not store your document or analysis results on the server.</li>
      </ul>
    </div>
  );
}

export default PrivacyNotice;