import { useState } from "react";

import FileUploader from "./components/FileUploader";
import ModeSelector from "./components/ModeSelector";
import PrivacyNotice from "./components/PrivacyNotice";
import ResultsView from "./components/ResultsView";
import { analyzeDocument } from "./services/api";
import { extractTextFromPdf } from "./services/pdfTextExtractor";

function App() {
  const [documentMode, setDocumentMode] = useState("research");
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setErrorMessage("Please select a PDF file first.");
      setResult(null);
      return;
    }

    setIsLoading(true);
    setErrorMessage("");
    setResult(null);

    try {
      const extractedText = await extractTextFromPdf(selectedFile);

      if (!extractedText || extractedText.trim().length === 0) {
        throw new Error("Could not extract text from this PDF.");
      }

      const response = await analyzeDocument(documentMode, extractedText);
      setResult(response.result);
    } catch (error) {
      setErrorMessage(error.message || "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "24px" }}>
      <h1>PDF Document Explainer</h1>
      <p>
        Analyze a PDF in different modes without uploading the PDF file itself.
      </p>

      <div style={{ display: "grid", gap: "16px", marginTop: "24px" }}>
        <ModeSelector
          value={documentMode}
          onChange={setDocumentMode}
          disabled={isLoading}
        />

        <FileUploader
          onFileSelect={setSelectedFile}
          disabled={isLoading}
        />

        {selectedFile && (
          <div>
            <strong>Selected file:</strong> {selectedFile.name}
          </div>
        )}

        <button onClick={handleAnalyze} disabled={isLoading || !selectedFile}>
          {isLoading ? "Analyzing..." : "Analyze document"}
        </button>

        <PrivacyNotice />
      </div>

      {errorMessage && (
        <div
          style={{
            marginTop: "24px",
            padding: "12px",
            border: "1px solid #d33",
            borderRadius: "6px",
            backgroundColor: "#fff5f5",
            color: "#a00",
          }}
        >
          <strong>Error:</strong> {errorMessage}
        </div>
      )}

      {result && <ResultsView result={result} />}
    </div>
  );
}

export default App;