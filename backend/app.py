import streamlit as st
import pandas as pd
from classifier import classify_prompts
from metrics import compute_metrics
from pyecharts.charts import Pie
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts


# Chart Generation Function;;
def create_task_chart(task_name, ai_percentage):

    ai_percentage = int(round(ai_percentage))
    user_percentage = round(100 - ai_percentage, 1)

    # Handle edge cases
    if ai_percentage == 0:
        data = [("You", 100)]
        colors = ["#FF69B4"]
    elif ai_percentage == 100:
        data = [("AI", 100)]
        colors = ["#BDBDBD"]
    else:
        data = [
            ("AI", ai_percentage),
            ("You", user_percentage)
        ]
        colors = ["#BDBDBD", "#FF69B4"]

    pie = (
        Pie(init_opts=opts.InitOpts(width="350px", height="350px"))
        .add(
            "",
            data,
            radius=["20%", "50%"]
        )
        .set_colors(colors)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=task_name,
                pos_left="center"
            )
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="inside",
                formatter="{b}\n{d}%",
                font_size=14
            )
        )
    )

    return pie

# COI Risk Label
def get_risk_level(score):

    if score <= 30:
        return "Healthy AI Usage 🟢"
    elif score <= 60:
        return "Moderate Reliance 🟡"
    elif score <= 80:
        return "High Reliance 🟠"
    else:
        return "Critical Overreliance 🔴"


# App User Int.
st.title("ChatTime — AI Dependency Analyzer")

st.write(
"""
Analyze how much cognitive work you outsource to AI.
Inspired by **Bloom's Taxonomy** and research on **Cognitive Offloading**.
"""
)

# Persist Prompt History
if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = ""
prompt_history = st.text_area(
    "Paste your ChatGPT prompt history (one prompt per line):",
    value=st.session_state.prompt_history,
    height=200
)
st.session_state.prompt_history = prompt_history

# Run Analysis
if st.button("Analyze Session"):

    prompts = [p.strip() for p in prompt_history.split("\n") if p.strip()]

    if len(prompts) == 0:
        st.warning("Please enter prompts.")

    else:
        # Run Classification
        categories = classify_prompts(prompts)

        # Compute Metrics
        results = compute_metrics(categories)
        percentages = results["percentages"]

        # Session Metrics
        st.header("Session Metrics")
        st.write(f"Total Prompts: {results['total']}")
        df = pd.DataFrame(
            {
                "Category": percentages.keys(),
                "AI Usage (%)": [int(round(v)) for v in percentages.values()]            }
        )
        df["AI Usage (%)"] = df["AI Usage (%)"].astype(str) + "%"
        st.table(df)

        # COI Score
        st.header("Cognitive Offloading Index")

        st.metric("COI Score", f"{results['coi']:.1f}/100")

        st.write(get_risk_level(results["coi"]))

        # Lower Order Cognitive Tasks
        st.header("Lower-Order Cognitive Tasks")
        col1, col2 = st.columns(2)
        with col1:
            repetitive_chart = create_task_chart(
                "Repetitive Tasks",
                percentages["Repetitive"]
            )
            st_pyecharts(repetitive_chart)
        with col2:
            info_chart = create_task_chart(
                "Information Retrieval",
                percentages["Information"]
            )
            st_pyecharts(info_chart)

        # Higher Order Cognitive Tasks
        st.header("Higher-Order Cognitive Tasks")
        col1, col2, col3 = st.columns(3)
        with col1:
            problem_chart = create_task_chart(
                "Problem Solving",
                percentages["Problem Solving"]
            )
            st_pyecharts(problem_chart)
        with col2:
            critical_chart = create_task_chart(
                "Critical Thinking",
                percentages["Critical Thinking"]
            )
            st_pyecharts(critical_chart)
        with col3:
            creativity_chart = create_task_chart(
                "Creativity",
                percentages["Creativity"]
            )
            st_pyecharts(creativity_chart)

        # Automation vs Thinking
        st.header("Automation vs Cognitive Work")
        st.pyplot(results["chart"])
        # Insight Summary
        st.header("AI Usage Insight")

        st.write(
        f"""
        Your session shows **{results['coi']:.1f}% cognitive offloading**.

        Higher scores indicate greater reliance on AI for complex reasoning,
        problem solving, and creative tasks.

        This system is inspired by cognitive science frameworks such as
        Bloom's Taxonomy and research on cognitive offloading.
        """
        )