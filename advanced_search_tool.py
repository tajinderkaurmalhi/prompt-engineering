import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool

# === Load API Key ===
load_dotenv()

# === Initialize Gemini LLM ===
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    temperature=0.7
)

# === DuckDuckGo Search Tool ===
search = DuckDuckGoSearchRun()

# === Calculator Tool ===
def calculator_tool_func(query: str) -> str:
    try:
        result = eval(query)
        return str(result)
    except Exception as e:
        return f"Error evaluating: {str(e)}"

calculator = Tool(
    name="Calculator",
    func=calculator_tool_func,
    description="Useful for basic math like addition, subtraction, multiplication, etc."
)

# === Initialize Agent ===
agent = initialize_agent(
    tools=[search, calculator],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# === Ask your question ===
question = "What is the capital of India and what is 2 + 2?"
response = agent.run(question)

print("\n🤖 Gemini Agent Response:\n", response)