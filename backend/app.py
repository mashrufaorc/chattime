import streamlit as st
from classifier import classify_prompts
from metrics import compute_metrics

st.title("ChatTime — AI Dependency Analyzer")

st.write(
"""
Analyze how much cognitive work you outsource to AI.
Inspired by Bloom's Taxonomy and Cognitive Offloading research.
"""
)

prompt_history = st.text_area(
"Paste your ChatGPT prompt history (one prompt per line):"
)

if st.button("Analyze Session"):

    prompts = [p.strip() for p in prompt_history.split("\n") if p.strip()]

    if len(prompts) == 0:
        st.warning("Please enter prompts.")
    else:

        categories = classify_prompts(prompts)
        results = compute_metrics(categories)

        st.subheader("Session Metrics")

        st.write(f"Total Prompts: {results['total']}")

        st.write(results["percentages"])

        st.subheader("Cognitive Offloading Index")

        st.metric("COI Score", f"{results['coi']:.1f}/100")

        st.subheader("Automation vs Cognitive Work")

        st.pyplot(results["chart"])

st.subheader("AI Usage Insight")

st.write(
f"""
Your session shows {results['coi']:.1f}% cognitive offloading.

Higher scores indicate greater reliance on AI for complex reasoning tasks.
"""
)

