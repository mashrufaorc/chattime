from google.genai import types
from app.gemini_client import get_genai_client
from app.config import settings
from app.schemas import AlignmentInput
from app.utils.similarity import cosine_similarity


def _embed_text(text: str) -> list[float]:
    client = get_genai_client()

    response = client.models.embed_content(
        model=settings.GEMINI_EMBED_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="SEMANTIC_SIMILARITY"
        ),
    )

    if hasattr(response, "embeddings") and response.embeddings:
        return response.embeddings[0].values

    return response["embeddings"][0]["values"]


def interpret_alignment(
    similarity: float,
    follow_up_count: int,
    self_attempt_detected: bool,
) -> str:
    if similarity >= 0.9 and follow_up_count <= 1 and not self_attempt_detected:
        return (
            "Your recap was extremely close to the AI response, with limited evidence of "
            "independent reasoning. This may indicate passive reliance rather than synthesis."
        )
    if similarity >= 0.8 and (follow_up_count >= 2 or self_attempt_detected):
        return (
            "Your recap closely matched the AI response, and your interaction included signs "
            "of active engagement. This suggests solid understanding rather than simple copying."
        )
    if 0.55 <= similarity < 0.8:
        return (
            "Your recap had moderate semantic overlap with the AI response. This often suggests "
            "healthy paraphrasing or partial synthesis in your own words."
        )
    if similarity < 0.55 and self_attempt_detected:
        return (
            "Your recap differed noticeably from the AI response, but you showed evidence of your "
            "own attempt. This may reflect independent thinking or reinterpretation."
        )
    return (
        "Your recap differed substantially from the AI response. This may indicate misunderstanding, "
        "distraction, or a need for more clarification."
    )


def analyze_alignment(data: AlignmentInput) -> dict:
    assistant_vec = _embed_text(data.assistant_text)
    user_vec = _embed_text(data.user_recap_text)

    sim = cosine_similarity(assistant_vec, user_vec)
    interpretation = interpret_alignment(
        similarity=sim,
        follow_up_count=data.follow_up_count,
        self_attempt_detected=data.self_attempt_detected,
    )

    return {
        "cosine_similarity": round(sim, 4),
        "interpretation": interpretation,
    }