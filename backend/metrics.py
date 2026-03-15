# Cognitive weights for COI calculation
weights = {
    "Repetitive": 0.2,
    "Information": 0.3,
    "Problem Solving": 0.7,
    "Critical Thinking": 0.9,
    "Creativity": 1.0
}

def compute_metrics(results):
    # Initialize totals
    totals = {
        "Repetitive": 0,
        "Information": 0,
        "Problem Solving": 0,
        "Critical Thinking": 0,
        "Creativity": 0
    }

    # Sum up all categories
    for r in results:
        for key in totals:
            totals[key] += r.get(key, 0)

    total_prompts = len(results)

    # Calculate percentages (average per prompt)
    
    percentages = {}
    for key in totals:
        percentages[key] = totals[key] / total_prompts if total_prompts > 0 else 0

    # Calculate Cognitive Offloading Index (COI)
    for k in weights:
        raw_score += totals[k] * weights[k] / 100

    coi = (raw_score / total_prompts) * 100

    automation =
    thinking = totals["Problem Solving"] + totals["Critical Thinking"] + totals["Creativity"]

    raw_score = 0
    for key in weights:
        raw_score += totals[key] * weights[key] / 100

    coi = (raw_score / total_prompts) * 100 if total_prompts > 0 else 0

    return {
        "total": total_prompts,
        "coi": coi,
        "percentages": percentages
    }