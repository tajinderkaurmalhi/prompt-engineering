import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Use Gemini 2.0 Flash
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_cpp_code(prompt):
    response = model.generate_content(prompt)
    return response.text

# Test
prompt = "Write a C++ program to print Fibonacci numbers up to 100."
print("Prompt:", prompt)
print("Generated C++ Code:\n", generate_cpp_code(prompt))