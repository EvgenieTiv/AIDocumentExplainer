from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analyze import router as analyze_router


app = FastAPI(title="PDF Document Explainer API")

# Backend: python -m uvicorn app.main:app --reload
# Frontend: npm run dev

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# подключаем роуты
app.include_router(analyze_router)


@app.get("/")
def root():
    return {
        "message": "PDF Document Explainer API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }