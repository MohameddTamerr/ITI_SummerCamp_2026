from pathlib import Path

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="AI Text Detector")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

model = joblib.load("./models/ai_text_classifier.joblib")


# ── Schemas ───────────────────────────────────────────────────────────────────

class TextRequest(BaseModel):
    text: str

    model_config = {
        "json_schema_extra": {"example": {"text": "The rise of AI is transforming every industry..."}}
    }


class PredictResponse(BaseModel):
    label: str       # "AI-generated" or "Human-written"
    confidence: float  # e.g. 0.947


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"name": "AI Text Classifier", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: TextRequest):
    prediction  = int(model.predict([request.text])[0])
    probability = model.predict_proba([request.text])[0]

    return PredictResponse(
        label="AI-generated" if prediction == 1 else "Human-written",
        confidence=float(probability[prediction]),
    )
