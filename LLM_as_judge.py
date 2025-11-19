import google.generativeai as genai

# Configure your API key
genai.configure(api_key="AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA")

# Use Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Task and responses
task = "Explain why reading books is beneficial for students."

response_a = "Reading improves vocabulary, boosts imagination, and helps students understand the world better."
response_b = "Students should read books because it is good and makes them smart."

# Judge prompt
judge_prompt = f"""
You are an expert language model acting as a judge.

Task:
{task}

Response A:
{response_a}

Response B:
{response_b}

Which response is better and why? Provide your answer in the following format:

Winner: A or B  
Reason: (Brief explanation)
"""

# Get judgment
result = model.generate_content(judge_prompt)
print("🤖 LLM-as-a-Judge Result:\n")
print(result.text)