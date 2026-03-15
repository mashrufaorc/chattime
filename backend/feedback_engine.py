import json
import os
import re
from typing import Any, Dict, List

try:
    from groq import Groq
except ImportError:  # pragma: no cover - runtime fallback for minimal environments
    Groq = None

from classifier import classify_prompts
from metrics import compute_metrics

CATEGORIES = [
    "Repetitive",
    "Information",
    "Problem Solving",
    "Critical Thinking",
    "Creativity",
]


def get_risk_level(score: float) -> str:
    if score <= 30:
        return "Healthy AI Usage"
    if score <= 60:
        return "Moderate Reliance"
    if score <= 80:
        return "High Reliance"
    return "Critical Overreliance"


def detect_patterns(percentages: Dict[str, float], coi: float) -> List[str]:
    patterns: List[str] = []

    lower_order = percentages["Repetitive"] + percentages["Information"]
    higher_order = (
        percentages["Problem Solving"]
        + percentages["Critical Thinking"]
        + percentages["Creativity"]
    )

    if lower_order >= 65:
        patterns.append(
            "You are using AI mostly for routine or retrieval-heavy tasks in this session."
        )
    if higher_order >= 45:
        patterns.append(
            "A large share of your prompts asks AI to support higher-order reasoning."
        )
    if percentages["Critical Thinking"] < 12:
        patterns.append(
            "Your prompts show limited explicit evaluation of trade-offs or alternatives."
        )
    if percentages["Creativity"] < 10:
        patterns.append(
            "There is little exploratory idea generation compared with execution requests."
        )
    if coi >= 60:
        patterns.append(
            "The current cognitive offloading level suggests meaningful dependence risk."
        )
    if not patterns:
        patterns.append(
            "Your session is fairly balanced between AI assistance and human reasoning."
        )

    return patterns


def _extract_json_object(raw: str) -> Dict[str, Any]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    cleaned = raw.strip()
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", cleaned)
    if not match:
        raise ValueError("Could not parse feedback JSON from model response.")
    return json.loads(match.group(0))


def _rule_based_feedback(
    percentages: Dict[str, float], coi: float, patterns: List[str]
) -> Dict[str, Any]:
    top_category = max(percentages, key=percentages.get)
    lower_order = percentages["Repetitive"] + percentages["Information"]
    higher_order = (
        percentages["Problem Solving"]
        + percentages["Critical Thinking"]
        + percentages["Creativity"]
    )

    current_behavior = (
        f"Your current session is led by {top_category} prompts "
        f"({percentages[top_category]:.1f}%), with {lower_order:.1f}% focused on "
        f"lower-order tasks and {higher_order:.1f}% on higher-order thinking."
    )

    likely_meaning = (
        f"This pattern maps to a {get_risk_level(coi).lower()} profile "
        f"(COI {coi:.1f}/100). It suggests AI is helping productivity, but some "
        f"core reasoning steps may be externalized."
    )

    next_session_improvements = [
        "Before asking AI for a full answer, write your own 2-3 step draft approach.",
        "Add one explicit trade-off question in each complex task (e.g., compare two methods).",
        "Use AI to critique or refine your reasoning rather than replacing first-pass thinking.",
    ]

    return {
        "current_behavior": current_behavior,
        "likely_meaning": likely_meaning,
        "next_session_improvements": next_session_improvements,
        "pattern_summary": patterns,
    }


def generate_personalized_feedback(
    prompts: List[str], percentages: Dict[str, float], coi: float, patterns: List[str]
) -> Dict[str, Any]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or Groq is None:
        return _rule_based_feedback(percentages, coi, patterns)

    client = Groq(api_key=api_key)
    sample_prompts = prompts[:8]

    system_message = """
You are ChatTime's cognitive feedback coach.
Convert AI chat behavior into concise, practical coaching.
Return valid JSON only.
"""
    user_message = f"""
Analyze this AI usage session and produce personalized feedback.

Session context:
- Prompt samples: {sample_prompts}
- Category percentages: {percentages}
- Cognitive Offloading Index (COI): {coi:.1f}
- Pattern signals: {patterns}

Return JSON with exactly these keys:
{{
  "current_behavior": "1-2 sentences describing what the user is doing now",
  "likely_meaning": "1-2 sentences explaining what this behavior likely means",
  "next_session_improvements": [
    "3 to 5 concrete actions the user can take in their next session"
  ]
}}
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            temperature=0.3,
            messages=[
                {"role": "system", "content": system_message.strip()},
                {"role": "user", "content": user_message.strip()},
            ],
        )
        content = response.choices[0].message.content
        parsed = _extract_json_object(content)

        if not isinstance(parsed.get("next_session_improvements"), list):
            raise ValueError("next_session_improvements must be a list")

        return {
            "current_behavior": str(parsed.get("current_behavior", "")).strip(),
            "likely_meaning": str(parsed.get("likely_meaning", "")).strip(),
            "next_session_improvements": [
                str(item).strip()
                for item in parsed.get("next_session_improvements", [])
                if str(item).strip()
            ],
            "pattern_summary": patterns,
        }
    except Exception:
        return _rule_based_feedback(percentages, coi, patterns)


def _normalize_scores(raw_scores: Dict[str, float]) -> Dict[str, float]:
    total = sum(raw_scores.values())
    if total <= 0:
        equal = 100 / len(CATEGORIES)
        return {category: equal for category in CATEGORIES}
    return {category: (value / total) * 100 for category, value in raw_scores.items()}


def _classify_prompts_fallback(prompts: List[str]) -> List[Dict[str, float]]:
    keyword_map = {
        "Repetitive": ["rewrite", "format", "summarize", "fix grammar", "email", "clean up"],
        "Information": ["what is", "explain", "define", "list", "when", "where", "who", "why"],
        "Problem Solving": ["debug", "error", "solve", "optimize", "issue", "bug", "implement"],
        "Critical Thinking": ["compare", "trade-off", "evaluate", "pros and cons", "best approach"],
        "Creativity": ["brainstorm", "idea", "design", "story", "creative", "innovative"],
    }

    fallback_results: List[Dict[str, float]] = []
    for prompt in prompts:
        lowered = prompt.lower()
        raw = {category: 1.0 for category in CATEGORIES}
        for category, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword in lowered:
                    raw[category] += 2.5
        fallback_results.append(_normalize_scores(raw))
    return fallback_results


def analyze_chat_session(prompts: List[str]) -> Dict[str, Any]:
    cleaned_prompts = [p.strip() for p in prompts if isinstance(p, str) and p.strip()]
    if not cleaned_prompts:
        raise ValueError("Prompt list is empty.")

    try:
        categories = classify_prompts(cleaned_prompts)
    except Exception:
        categories = _classify_prompts_fallback(cleaned_prompts)
    metrics = compute_metrics(categories)
    percentages = {k: round(v, 1) for k, v in metrics["percentages"].items()}

    automation_tasks = round(percentages["Repetitive"] + percentages["Information"], 1)
    cognitive_tasks = round(
        percentages["Problem Solving"]
        + percentages["Critical Thinking"]
        + percentages["Creativity"],
        1,
    )
    coi = round(metrics["coi"], 1)

    patterns = detect_patterns(percentages, coi)
    feedback = generate_personalized_feedback(cleaned_prompts, percentages, coi, patterns)

    return {
        "total_prompts": len(cleaned_prompts),
        "percentages": percentages,
        "automation_tasks": automation_tasks,
        "cognitive_tasks": cognitive_tasks,
        "coi": coi,
        "risk_level": get_risk_level(coi),
        "feedback": feedback,
    }