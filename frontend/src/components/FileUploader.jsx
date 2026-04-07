function FileUploader({ onFileSelect, disabled = false }) {
  const handleChange = (event) => {
    const selectedFile = event.target.files?.[0] || null;

    if (!selectedFile) {
      onFileSelect(null);
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      alert("Please select a PDF file.");
      event.target.value = "";
      onFileSelect(null);
      return;
    }

    onFileSelect(selectedFile);
  };

  return (
    <div>
      <label htmlFor="pdf-file">PDF file</label>
      <br />
      <input
        id="pdf-file"
        type="file"
        accept="application/pdf"
        onChange={handleChange}
        disabled={disabled}
      />
    </div>
  );
}

export default FileUploader;