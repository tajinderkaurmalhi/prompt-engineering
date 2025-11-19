import google.generativeai as genai
from dotenv import load_dotenv
import os

# === Load Gemini API Key ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# === Initialize Gemini Model ===
model = genai.GenerativeModel("gemini-1.5-flash")

# === Memory Buffer ===
conversation_history = []


# === Function to simulate memory ===
def ask_with_memory(user_input):
    global conversation_history
    full_prompt = ""

    # Append all previous conversation to prompt
    for turn in conversation_history:
        full_prompt += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"

    # Add current user input
    full_prompt += f"User: {user_input}\nAssistant:"

    # Get response from Gemini
    response = model.generate_content(full_prompt)
    output = response.text.strip()

    # Save to memory
    conversation_history.append({
        "user": user_input,
        "assistant": output
    })

    return output


# === Multi-turn Conversation ===
print(ask_with_memory("Who is the current Prime Minister of the UK?"))
print(ask_with_memory("What is their educational background?"))
print(ask_with_memory("How old are they?"))
print(ask_with_memory("What political party do they belong to?"))