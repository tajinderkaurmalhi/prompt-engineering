import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper

# Load API key from .env
load_dotenv()

# Gemini 1.5 Flash initialization
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    temperature=0.7
)

# Wikipedia tool
wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# Create Agent with Wikipedia + Gemini
agent = initialize_agent(
    tools=[wiki_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run the agent
question = "What is the history of the Eiffel Tower?"
response = agent.run(question)

print("\n📘 Gemini Agent Response:\n", response)