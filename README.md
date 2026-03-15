# ChatTime

Absolutely — here’s a more polished, hackathon-style `README.md` that sounds stronger on GitHub and is better for recruiters, judges, and anyone visiting the repo.

````markdown
# ChatTime AI Analyzer

ChatTime is an AI-powered cognitive analytics tool that helps users understand how they use AI — and how much thinking they may be offloading to it.

As AI tools become more integrated into daily life, people increasingly rely on them for rewriting, summarizing, brainstorming, coding, and decision support. ChatTime turns that behavior into something measurable. By analyzing prompt history through a Bloom’s Taxonomy–inspired framework, it generates an AI Dependency Report** that shows whether a user is using AI as a helpful tool — or leaning on it as a crutch.

---

## Why ChatTime?

The project began with a simple but uncomfortable observation:

> AI is becoming so convenient that many of us skip the thinking step entirely.

We paste emails, ask for rewrites, request summaries, and rely on AI for tasks we used to reason through ourselves. That raised deeper questions:

- What cognitive tasks are we offloading?
- How much thinking are we delegating?
- At what point does convenience become cognitive dependency?

ChatTime is a mirror for your AI habits.

---

## What It Does

ChatTime analyzes a user’s prompt history and classifies each prompt into five cognitive categories:

- Repetitive
- Information Retrieval
- Problem Solving
- Critical Thinking
- Creativity

It then groups these into AI Automation Tasks vs Human Cognitive Tasks, computes a Cognitive Offloading Index (COI), and generates a report showing:

- how much thinking the user did
- how much thinking the AI assistant did
- whether the user’s reliance is healthy, moderate, high, or critical
- a visualization of cognitive vs automated work
- actionable feedback and recommendations

---

## Key Features

- Bloom’s Taxonomy–inspired prompt classification
- Cognitive Offloading Index (COI) scoring
- AI vs Human cognitive task breakdown
- Insightful dependency analysis and recommendations
- Streamlit-based interactive interface
- Visualization layer for cognitive work distribution

---

## How It Works

The ChatTime pipeline consists of the following stages:

1. Prompt Parser 
   Cleans and segments a user’s prompt history.

2. Classification Engine  
   Uses LLM-based analysis to map prompts to cognitive categories.

3. Metric Calculation Engine  
   Computes percentages and the Cognitive Offloading Index (COI) using weighted scoring.

4. Visualization Layer  
   Displays AI-vs-Human cognitive work in an intuitive visual format.

5. Insight Generator  
   Produces a human-readable report with personalized feedback and recommendations.

---

## Tech Stack

- Frontend / App Interface: Streamlit
- Backend: Python
- LLM Inference: Groq API
- Design Framework: Bloom’s Taxonomy / cognitive offloading principles

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mashrufaorc/chattime-ai-analyzer.git
cd chattime-ai-analyzer
````

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the root directory

Add your Groq API key to a `.env` file in the **root directory** of the project:

```env
GROQ_API_KEY=your_groq_api_key_here
```

You can generate your API key from Groq Console:

`https://console.groq.com/home`

### 5. Run the app

```bash
streamlit run app.py
```

---

## Environment Variables

The following environment variable is required:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Make sure the `.env` file is placed in the **root directory** of the project.

---

## Project Structure

```bash
chattime-ai-analyzer/
├── backend/
├── frontend/
└── README.md
```

> Update this structure if your final repository layout changes.

---

## Challenges We Faced

Building ChatTime was not just a technical challenge — it was also a conceptual one.

* **Defining cognitive categories:** Human thinking is messy, and many prompts do not fit cleanly into one box.
* **Weighting the COI:** Choosing weights that reflect cognitive effort required balancing theory with practical usability.
* **Handling ambiguous prompts:** Many prompts naturally span multiple cognitive levels at once.
* **Integrating the feedback system with Vertex AI through Google Cloud:** One of the biggest technical hurdles was connecting the feedback system to Vertex AI on Google Cloud.
* Although we later got the backend feedback pipeline working, **integrating that feedback system smoothly into the frontend was not completed within hackathon time constraints**.

---

## Accomplishments We’re Proud Of

* Creating a quantifiable way to measure **AI cognitive offloading**
* Designing a COI metric that is both intuitive and academically grounded
* Turning raw prompt histories into meaningful cognitive insights
* Building a strong foundation for a future AI usage feedback platform
* Prototyping a system with real potential as a **browser extension or ChatGPT plugin**

---

## What We Learned

* AI usage is not just about productivity — it shapes how people think
* Users often underestimate how much cognitive work they outsource until they see it visualized
* Bloom’s Taxonomy adapts surprisingly well to modern AI interaction analysis
* Cloud integration and user-facing product design can be harder than getting the model pipeline working

---

## What’s Next

We see ChatTime as the beginning of a larger platform for reflective, responsible AI use.

Future directions include:

* full frontend integration of the feedback system
* **A/B testing** to compare which recommendation styles most effectively influence healthier AI usage
* **cosine similarity–based feedback matching** to compare current user behavior to known cognitive usage profiles
* longitudinal tracking across weeks and months
* personalized recommendations to rebalance cognitive habits
* browser extension / ChatGPT plugin integration
* privacy-preserving local analysis
* team and organization dashboards

---

## Demo

[Watch the demo](https://youtu.be/e-XvpDiv4WE)

---

## GitHub Repository

[ChatTime AI Analyzer](https://github.com/mashrufaorc/chattime-ai-analyzer)

---

## Long-Term Vision

Our long-term goal is to help people use AI as a **tool rather than a crutch** and keep **human cognition at the center of the loop**.

---


