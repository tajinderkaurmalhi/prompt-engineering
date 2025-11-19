import google.generativeai as genai
from dotenv import load_dotenv
import os

# === Load Gemini API Key ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# === Initialize Gemini Model ===
model = genai.GenerativeModel("gemini-1.5-flash")

# === Multiline Input Helper ===
def read_multiline_input(prompt):
    print(prompt)
    print("👉 Paste your code. Press Enter twice to finish.")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

# === 1. Generate Simple C++ Code ===
def generate_cpp_code(task_prompt):
    engineered_prompt = (
        "You are an expert C++ developer. Write a very simple, clean and readable C++ code for the following task:\n\n"
        + task_prompt
    )
    response = model.generate_content(engineered_prompt)
    return response.text

# === 2. Optimize C++ Code ===
def optimize_cpp_code(code):
    prompt = (
        "Optimize the following C++ code for readability, performance, and simplicity. Add comments where necessary:\n\n"
        + code
    )
    response = model.generate_content(prompt)
    return response.text

# === 3. Debug C++ Code ===
def debug_cpp_code(code):
    prompt = (
        "The following C++ code contains bugs. Fix them and explain the changes:\n\n"
        + code
    )
    response = model.generate_content(prompt)
    return response.text

# === Main App Logic ===
def main():
    print("\n🧠 Welcome to Gemini C++ Assistant (Full Flow)")

    # Step 1: C++ Code Generation
    task = input("\n💬 Enter the task you want a C++ program for: ")
    generated_code = generate_cpp_code(task)
    print("\n✅ Generated Simple C++ Code:\n", generated_code)

    # Step 2: Ask if user wants optimization
    choice_opt = input("\n⚙️ Do you want to optimize this code? (y/n): ").strip().lower()
    if choice_opt == "y":
        optimized_code = optimize_cpp_code(generated_code)
        print("\n🚀 Optimized C++ Code:\n", optimized_code)
    else:
        optimized_code = generated_code

    # Step 3: Ask if user wants debugging
    choice_debug = input("\n🧪 Do you want to debug this code? (y/n): ").strip().lower()
    if choice_debug == "y":
        use_last = input("🔍 Use the above optimized/generated code? (y/n): ").strip().lower()
        if use_last == "y":
            code_to_debug = optimized_code
        else:
            code_to_debug = read_multiline_input("\n📥 Paste your buggy C++ code:")
        debugged_code = debug_cpp_code(code_to_debug)
        print("\n🔧 Debugged Code and Explanation:\n", debugged_code)

    print("\n✅ Session complete. You can re-run for another task.")

# === Run It ===
if __name__ == "__main__":
    main()