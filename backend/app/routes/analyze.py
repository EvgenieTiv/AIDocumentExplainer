from fastapi import APIRouter, HTTPException

from app.schemas.requests import AnalyzeDocumentRequest
from app.schemas.responses import AnalyzeDocumentResponse
from app.services.document_processor import summarize_document_to_json


router = APIRouter()


@router.post("/analyze", response_model=AnalyzeDocumentResponse)
def analyze_document(payload: AnalyzeDocumentRequest):
    try:
        result = summarize_document_to_json(
            document_mode=payload.document_mode,
            document_text=payload.document_text,
        )

        return AnalyzeDocumentResponse(
            document_mode=payload.document_mode,
            result=result,
        )

    except ValueError as e:
        print("ValueError in /analyze:", repr(e))
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print("Unhandled exception in /analyze:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze document: {str(e)}"
        )