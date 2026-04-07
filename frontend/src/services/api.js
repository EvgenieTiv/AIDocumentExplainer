const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function analyzeDocument(documentMode, documentText) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      document_mode: documentMode,
      document_text: documentText,
    }),
  });

  if (!response.ok) {
    let errorMessage = "Failed to analyze document";

    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // ignore
    }

    throw new Error(errorMessage);
  }

  return response.json();
}