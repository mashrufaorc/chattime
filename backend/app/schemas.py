from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    text: str


class SessionInput(BaseModel):
    session_id: str
    user_id: str
    messages: List[ChatMessage]


class PromptLabel(BaseModel):
    index: int
    label: str
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str


class BehavioralScores(BaseModel):
    reasoning: int = Field(ge=0, le=100)
    critical_engagement: int = Field(ge=0, le=100)
    dependency_risk: int = Field(ge=0, le=100)
    repetitive_task_reliance: int = Field(ge=0, le=100)


class BehavioralAnalysis(BaseModel):
    session_summary: str
    behavioral_scores: BehavioralScores
    prompt_labels: List[PromptLabel]
    strengths: List[str]
    risks: List[str]
    recommended_feedback: List[str]


class AlignmentInput(BaseModel):
    session_id: str
    assistant_text: str
    user_recap_text: str
    follow_up_count: int = 0
    self_attempt_detected: bool = False


class AlignmentOutput(BaseModel):
    cosine_similarity: float
    interpretation: str


class ABInput(BaseModel):
    user_id: str
    session_id: str
    dependency_score: int
    reasoning_score: int


class ABOutput(BaseModel):
    variant: Literal["A_standard", "B_reflective"]
    intervention_title: str
    intervention_text: str


class ABEffectivenessInput(BaseModel):
    user_id: str
    variant: Literal["A_standard", "B_reflective"]
    baseline_dependency_score: int
    new_dependency_score: int
    baseline_reasoning_score: int
    new_reasoning_score: int


class ABEffectivenessOutput(BaseModel):
    variant: str
    dependency_delta: int
    reasoning_delta: int
    interpretation: str