import google.generativeai as genai

# Configure your API key
genai.configure(api_key="AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA")

# Initialize Gemini Flash
model = genai.GenerativeModel("gemini-1.5-flash")

# Define original and slightly modified prompts
prompts = {
    "original": "What causes climate change?",
    "sensitivity_1": "Can you tell me what causes climate change?",
    "sensitivity_2": "In your opinion, what causes climate change?",
    "sensitivity_3": "Please explain what causes climate change.",
    "sensitivity_4": "What are the causes of climate change, if any?"
}

# Collect responses
print("🧪 Sensitivity Testing Results:\n")
responses = {}

for label, prompt in prompts.items():
    response = model.generate_content(prompt)
    responses[label] = response.text
    print(f"🔹 {label} prompt:\n{prompt}")
    print(f"📘 Response:\n{response.text}\n{'-'*60}")