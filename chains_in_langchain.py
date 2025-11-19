import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variable
load_dotenv()

# Initialize Gemini model (Flash)
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    temperature=0.7
)

# Create a Prompt Template
prompt = PromptTemplate(
    input_variables=["food_item"],
    template="What are the health benefits of eating {food_item}?"
)

# Create a Chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run the Chain
response = chain.run("banana")

print("Gemini Response:", response)