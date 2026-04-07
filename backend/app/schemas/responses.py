from typing import Any, Dict

from pydantic import BaseModel, Field


class AnalyzeDocumentResponse(BaseModel):
    document_mode: str = Field(..., description="Document analysis mode used")
    result: Dict[str, Any] = Field(..., description="Structured analysis result")