import hashlib
from app.schemas import ABInput, ABEffectivenessInput


def assign_variant(user_id: str) -> str:
    digest = hashlib.sha256(user_id.encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 2
    return "A_standard" if bucket == 0 else "B_reflective"


def get_intervention(data: ABInput) -> dict:
    variant = assign_variant(data.user_id)

    if variant == "A_standard":
        return {
            "variant": "A_standard",
            "intervention_title": "Standard Feedback",
            "intervention_text": (
                "Try attempting the first step on your own before asking AI for the full answer."
            ),
        }

    return {
        "variant": "B_reflective",
        "intervention_title": "Reflective Coaching",
        "intervention_text": (
            "Before using AI next time, pause and write 2 steps of your own reasoning first. "
            "Then ask AI to critique or extend your thinking instead of replacing it."
        ),
    }


def measure_effectiveness(data: ABEffectivenessInput) -> dict:
    dependency_delta = data.new_dependency_score - data.baseline_dependency_score
    reasoning_delta = data.new_reasoning_score - data.baseline_reasoning_score

    if dependency_delta < 0 and reasoning_delta > 0:
        interpretation = (
            "This intervention appears effective: dependency signals decreased while reasoning increased."
        )
    elif dependency_delta < 0:
        interpretation = (
            "This intervention reduced dependency signals, though reasoning gains were limited."
        )
    elif reasoning_delta > 0:
        interpretation = (
            "This intervention improved reasoning behavior, though dependency signals did not decrease."
        )
    else:
        interpretation = (
            "This intervention showed limited positive change in the observed session-to-session behavior."
        )

    return {
        "variant": data.variant,
        "dependency_delta": dependency_delta,
        "reasoning_delta": reasoning_delta,
        "interpretation": interpretation,
    }