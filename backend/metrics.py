import matplotlib.pyplot as plt
from collections import Counter

weights = {
    "Repetitive": 0.2,
    "Information": 0.4,
    "Problem Solving": 0.7,
    "Critical Thinking": 0.9,
    "Creativity": 1.0
}

def compute_metrics(categories):

    counts = Counter(categories)
    total = len(categories)

    repetitive = counts["Repetitive"]
    information = counts["Information"]
    problem = counts["Problem Solving"]
    critical = counts["Critical Thinking"]
    creativity = counts["Creativity"]

    raw_score = (
        repetitive * 0.2 +
        information * 0.4 +
        problem * 0.7 +
        critical * 0.9 +
        creativity * 1.0
    )

    coi = (raw_score / total) * 100

    automation = repetitive + information
    thinking = problem + critical + creativity

    fig, ax = plt.subplots()
    ax.pie(
        [automation, thinking],
        labels=["AI Automation Tasks", "Human Cognitive Tasks"],
        autopct="%1.1f%%"
    )

    percentages = {
        "Repetitive": repetitive / total * 100,
        "Information": information / total * 100,
        "Problem Solving": problem / total * 100,
        "Critical Thinking": critical / total * 100,
        "Creativity": creativity / total * 100,
    }

    return {
        "total": total,
        "coi": coi,
        "percentages": percentages,
        "chart": fig
    }
