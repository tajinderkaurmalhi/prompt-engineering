import google.generativeai as genai
import time

# Configure your Gemini API key
genai.configure(api_key="AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA")

# Use Gemini 1.5 Flash
model = genai.GenerativeModel("gemini-1.5-flash")

# Prompt to test
prompt = "Explain why teamwork is important in school projects."

# Generate multiple responses
print("🎯 Response Diversity Testing (Same Prompt, Multiple Generations):\n")

responses = []
num_trials = 5  # Number of times to test

for i in range(num_trials):
    response = model.generate_content(prompt)
    responses.append(response.text)
    print(f"🔁 Attempt {i+1}:\n{response.text}\n{'-'*60}")
    time.sleep(1)  # Optional: to avoid