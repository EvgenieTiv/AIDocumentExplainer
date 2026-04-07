from pydantic import BaseModel, Field


class AnalyzeDocumentRequest(BaseModel):
    document_mode: str = Field(..., description="Document analysis mode")
    document_text: str = Field(..., min_length=1, description="Extracted document text")