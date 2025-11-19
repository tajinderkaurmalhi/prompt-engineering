import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key="AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA")

# Use Gemini Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# --------------------------
# ZERO-SHOT PROMPT
# --------------------------
zero_shot_prompt = "What is the capital of France?"

# --------------------------
# FEW-SHOT PROMPT
# --------------------------
few_shot_prompt = """
Q: What is the capital of Germany?
A: Berlin

Q: What is the capital of Japan?
A: Tokyo

Q: What is the capital of Brazil?
A: Brasília

Q: What is the capital of France?
A:"""

# --------------------------
# Generate Responses
# --------------------------
print("🔵 Zero-Shot Prompt:\n", zero_shot_prompt)
zero_shot_response = model.generate_content(zero_shot_prompt)
print("🧠 Response (Zero-Shot):\n", zero_shot_response.text)
print("=" * 60)

print("🟢 Few-Shot Prompt:\n", few_shot_prompt)
few_shot_response = model.generate_content(few_shot_prompt)
print("🧠 Response (Few-Shot):\n", few_shot_response.text)
print("=" * 60)