from google.genai import types
from app.gemini_client import get_genai_client
from app.config import settings
from app.schemas import SessionInput


BEHAVIOR_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "session_summary": {"type": "STRING"},
        "behavioral_scores": {
            "type": "OBJECT",
            "properties": {
                "reasoning": {"type": "INTEGER"},
                "critical_engagement": {"type": "INTEGER"},
                "dependency_risk": {"type": "INTEGER"},
                "repetitive_task_reliance": {"type": "INTEGER"}
            },
            "required": [
                "reasoning",
                "critical_engagement",
                "dependency_risk",
                "repetitive_task_reliance"
            ]
        },
        "prompt_labels": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "index": {"type": "INTEGER"},
                    "label": {"type": "STRING"},
                    "confidence": {"type": "NUMBER"},
                    "explanation": {"type": "STRING"}
                },
                "required": ["index", "label", "confidence", "explanation"]
            }
        },
        "strengths": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "risks": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "recommended_feedback": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        }
    },
    "required": [
        "session_summary",
        "behavioral_scores",
        "prompt_labels",
        "strengths",
        "risks",
        "recommended_feedback"
    ]
}


def _build_session_text(session: SessionInput) -> str:
    return "\n".join(
        f"{i}. {msg.role.upper()}: {msg.text}"
        for i, msg in enumerate(session.messages)
    )


def analyze_behavior(session: SessionInput) -> dict:
    client = get_genai_client()
    session_text = _build_session_text(session)

    system_prompt = """
You are an analyst for an AI-usage feedback platform called Chattime.

Analyze the user's chat behavior, not the correctness of the answer.

Focus on:
1. reasoning behavior
2. critical engagement
3. dependency risk
4. repetitive-task reliance
5. whether the user is using AI as a learning partner or a thinking replacement

Scoring guidance:
- reasoning is high when the user breaks problems down, asks why/how, compares ideas, or attempts their own answer
- critical_engagement is high when the user questions, critiques, or reflects on answers
- dependency_risk is high when the user repeatedly requests final answers, complete outputs, or no-effort solutions
- repetitive_task_reliance is high when prompts are mostly formatting, summarizing, rewriting, or automation

Allowed prompt labels include:
- direct_solution_request
- clarification_request
- brainstorming
- rewriting_or_formatting
- reflective_summary
- self_attempt
- critique_or_verification
- repetitive_automation
- research_guidance
- planning_or_structuring

Return JSON only.
""".strip()

    response = client.models.generate_content(
        model=settings.GEMINI_TEXT_MODEL,
        contents=[
            system_prompt,
            f"Analyze this session:\n\n{session_text}"
        ],
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
            response_schema=BEHAVIOR_SCHEMA
        )
    )

    return response.parsed if response.parsed else response.json()