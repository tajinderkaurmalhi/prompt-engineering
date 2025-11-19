import pandas as pd
import json
import os
from dotenv import load_dotenv

# Load .env API key
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Sample C++ dataset for prompt-code completion
data = [
    {
        "prompt": "Write a C++ program to add two numbers.",
        "completion": "#include<iostream>\nusing namespace std;\nint main() {\n  int a = 5, b = 10;\n  cout << a + b;\n  return 0;\n}"
    },
    {
        "prompt": "Write a C++ function to check if a number is prime.",
        "completion": "bool isPrime(int n) {\n  if(n <= 1) return false;\n  for(int i=2; i*i<=n; i++)\n    if(n % i == 0) return false;\n  return true;\n}"
    }
]

# Save to DataFrame
df = pd.DataFrame(data)
df.to_csv("cpp_code_generation.csv", index=False)

# Convert to JSONL format
def save_jsonl(df, filename):
    with open(filename, "w") as f:
        for _, row in df.iterrows():
            entry = {
                "messages": [
                    {"role": "user", "content": row['prompt']},
                    {"role": "model", "content": row['completion']}
                ]
            }
            f.write(json.dumps(entry) + "\n")

# 80-20 split
train_df = df.sample(frac=0.8, random_state=42)
test_df = df.drop(train_df.index)

save_jsonl(train_df, "train_cpp.jsonl")
save_jsonl(test_df, "test_cpp.jsonl")