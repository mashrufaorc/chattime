from groq import Groq
import os
import json
import re

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    api_key = api_key.strip()
    print(f"Classifier API Key loaded (length: {len(api_key)})")
else:
    print("WARNING: GROQ_API_KEY not found in classifier")

client = Groq(api_key=api_key)

def classify_prompts(prompts):
    results = []

    for prompt in prompts:
        try:
            message = f"""
            You are a cognitive science expert analyzing how humans outsource thinking to AI.
            Your reasoning framework is based on Bloom's Taxonomy, which consists of the following cognitive levels, ordered from higher-order to lower-order thinking: creating, evaluating, analyzing, applying, understanding, and remembering. 
            Our system simplifies Bloom’s taxonomy into five practical AI interaction categories:
            1.)Repetitive Tasks ->  Remembering/Understanding
            2.)Information Retrieval --> Remembering/Understanding
            3.)Problem Solving  --> Applying/Analyzing/Evaluating
            4.)Critical Thinking  --> Analyzing/Evaluating
            5.)Creativity -> Creating 
            A single prompt may involve multiple cognitive processes. Therefore you must distribute percentages across categories.

            5 Categories are listed below with example descriptions for each:
            1.)Repetitive: Editing, formatting, rewriting, summarizing text.
            2.)Information: Requesting explanations or factual knowledge.
            3.) Problem Solving: Debugging, troubleshooting, or solving technical/logical problems.
            4.) Critical Thinking: Comparing ideas, evaluating strategies, reasoning through tradeoffs.
            5.) Creativity: Generating new ideas, designs, concepts, or original content.

            Instructions:
            1. Analyze the cognitive processes required in the prompt.
            2. Assign percentages across the categories.
            3. Percentages must sum to 100.
            4. If only one category applies, assign 100%.

            Return JSON ONLY in this format:

            {{
            "Repetitive": number,
            "Information": number,
            "Problem Solving": number,
            "Critical Thinking": number,
            "Creativity": number
            }}

            Prompt:
            {prompt}
            
            You are a cognitive science expert analyzing how humans outsource thinking to AI.
            Your reasoning framework is based on Bloom's Taxonomy, which consists of the following cognitive levels, ordered from higher-order to lower-order thinking: creating, evaluating, analyzing, applying, understanding, and remembering. 
            Our system simplifies Bloom’s taxonomy into five practical AI interaction categories:
            1.)Repetitive Tasks ->  Remembering/Understanding
            2.)Information Retrieval --> Remembering/Understanding
            3.)Problem Solving  --> Applying/Analyzing/Evaluating
            4.)Critical Thinking  --> Analyzing/Evaluating
            5.)Creativity -> Creating 
            A single prompt may involve multiple cognitive processes. Therefore you must distribute percentages across categories.

            5 Categories are listed below with example descriptions for each:
            1.)Repetitive: Editing, formatting, rewriting, summarizing text.
            2.)Information: Requesting explanations or factual knowledge.
            3.) Problem Solving: Debugging, troubleshooting, or solving technical/logical problems.
            4.) Critical Thinking: Comparing ideas, evaluating strategies, reasoning through tradeoffs.
            5.) Creativity: Generating new ideas, designs, concepts, or original content.

            Instructions:
            1. Analyze the cognitive processes required in the prompt.
            2. Assign percentages across the categories.
            3. Percentages must sum to 100.
            4. If only one category applies, assign 100%.

            Return JSON ONLY in this format:

            {{
            "Repetitive": number,
            "Information": number,
            "Problem Solving": number,
            "Critical Thinking": number,
            "Creativity": number
            }}

            Prompt:
            {prompt}
                """

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Make sure this model is available in your Groq account
                messages=[{"role": "user", "content": message}],
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean the response
            content = re.sub(r'```json\s*|\s*```', '', content)
            content = content.strip()
            
            try:
                data = json.loads(content)
                # Ensure all keys exist
                default_data = {
                    "Repetitive": 0,
                    "Information": 0,
                    "Problem Solving": 0,
                    "Critical Thinking": 0,
                    "Creativity": 0
                }
                default_data.update(data)
                results.append(default_data)
                
            except json.JSONDecodeError:
                # Fallback distribution
                results.append({
                    "Repetitive": 0,
                    "Information": 0,
                    "Problem Solving": 0,
                    "Critical Thinking": 0,
                    "Creativity": 0
                })

        except Exception as e:
            print(f"Error classifying prompt: {str(e)}")
            results.append({
                "Repetitive": 0,
                "Information": 0,
                "Problem Solving": 0,
                "Critical Thinking": 0,
                "Creativity": 0
            })

    return results