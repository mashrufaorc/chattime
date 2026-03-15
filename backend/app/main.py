from fastapi import FastAPI
from app.config import settings
from app.schemas import (
    SessionInput,
    AlignmentInput,
    ABInput,
    ABEffectivenessInput,
)
from app.services.behavior_service import analyze_behavior
from app.services.alignment_service import analyze_alignment
from app.services.ab_service import get_intervention, measure_effectiveness

app = FastAPI(title="Chattime Backend")


@app.on_event("startup")
def startup_check():
    if not settings.GOOGLE_CLOUD_PROJECT:
        raise ValueError("GOOGLE_CLOUD_PROJECT is missing in .env")


@app.get("/")
def root():
    return {"status": "ok", "service": "chattime-backend"}


@app.post("/analyze-session")
def analyze_session(payload: SessionInput):
    return analyze_behavior(payload)


@app.post("/understanding-alignment")
def understanding_alignment(payload: AlignmentInput):
    return analyze_alignment(payload)


@app.post("/ab-feedback")
def ab_feedback(payload: ABInput):
    return get_intervention(payload)


@app.post("/ab-results")
def ab_results(payload: ABEffectivenessInput):
    return measure_effectiveness(payload)