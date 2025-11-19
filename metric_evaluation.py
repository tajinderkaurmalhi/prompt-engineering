# === Auto_Evaluation.py ===

import google.generativeai as genai
from evaluate import load

# ✅ Paste your API key here
api_key = "AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# === Prompt and Reference ===
prompt = "Explain AI to a 5-year-old."
reference = "AI is like a smart robot that learns things just like kids learn."

response = model.generate_content(prompt).text

# === Evaluation
rouge = load("rouge")
bleu = load("bleu")

rouge_result = rouge.compute(predictions=[response], references=[reference])
bleu_result = bleu.compute(predictions=[response], references=[reference])

print("Generated:", response)
print("\nROUGE Score:", rouge_result)
print("BLEU Score:", bleu_result)