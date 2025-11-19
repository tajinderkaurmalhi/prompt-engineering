# === Human_Evaluation.py ===

import google.generativeai as genai

# ✅ Paste your API key here
api_key = "AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA"  # 🔐 Replace with your actual Gemini API key

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# === Prompts to Evaluate ===
prompts = ["Explain AI to a 5-year-old.", "Write a poem about the moon."]

responses = []
for prompt in prompts:
    response = model.generate_content(prompt)
    responses.append(response.text)

# === Simulated Human Ratings ===
human_ratings = [4.5, 3.8]

# === Display Output ===
for i, r in enumerate(responses):
    print(f"\nPrompt: {prompts[i]}\nResponse:\n{r}\nRating: {human_ratings[i]}/5\n")