from flask import Flask, request, jsonify
from flask_cors import CORS
from classifier import classify_prompts
from metrics import compute_metrics
from groq import Groq
import os

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    api_key = api_key.strip()
    print(f"API Key loaded successfully (length: {len(api_key)})")
else:
    print("ERROR: GROQ_API_KEY not set!")
    exit(1)

client = Groq(api_key=api_key)

# Initialize Flask
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    # Handle preflight requests
    if request.method == "OPTIONS":
        return "", 200
        
    try:
        data = request.json
        prompts = data.get("prompts", [])

        if not prompts:
            return jsonify({"error": "No prompts provided"}), 400

        prompt_text = prompts[0]

        # Get ACTUAL AI answer to the user's prompt
        ai_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt_text}]
        )
        answer = ai_response.choices[0].message.content

        # Also classify the prompt for metrics
        categories = classify_prompts(prompts)
        results = compute_metrics(categories)

        # Format response
        percentages = results["percentages"]
        
        # Calculate automation and thinking totals
        automation = percentages["Repetitive"] + percentages["Information"]
        thinking = percentages["Problem Solving"] + percentages["Critical Thinking"] + percentages["Creativity"]

        response_data = {
            "answer": answer,  # This is the actual AI response
            "automation": round(automation),
            "thinking": round(thinking),
            "coi": round(results["coi"], 1),
            "percentages": {
                "Repetitive": round(percentages["Repetitive"]),
                "Information": round(percentages["Information"]),
                "Problem Solving": round(percentages["Problem Solving"]),
                "Critical Thinking": round(percentages["Critical Thinking"]),
                "Creativity": round(percentages["Creativity"])
            },
            "total_prompts": results["total"]
        }
        
        print(f"Prompt: {prompt_text[:50]}...")
        print(f"Response sent with answer length: {len(answer)}")
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error in analyze endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)