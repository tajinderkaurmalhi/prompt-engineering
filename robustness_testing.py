import google.generativeai as genai

# Configure your API key
genai.configure(api_key="")

# Initialize Gemini Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Base prompt and its variations
prompts = {
    "original": "What are the benefits of learning a second language?",
    "variation_1": "List some advantages of knowing more than one language.",
    "variation_2": "Can you explain why learning a second language is useful?",
    "variation_3": "What good things happen when someone learns another language?",
    "variation_4": "Give reasons why people should study a new language."
}

# Generate and print responses
print("🧪 Robustness Testing:\n")
responses = {}

for label, prompt in prompts.items():
    response = model.generate_content(prompt)
    responses[label] = response.text
    print(f"🔹 {label} prompt:\n{prompt}")
    print(f"📘 Response:\n{response.text}\n{'-'*60}")

# You can later evaluate these responses:
# - Are they consistent?
# - Are key facts retained?
# - Does tone change too much?
# - Is quality stable?