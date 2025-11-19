import os
import requests
import warnings
from dotenv import load_dotenv

from langchain.agents import Tool, initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType

# Optional: suppress deprecation warning
warnings.filterwarnings("ignore", category=UserWarning)

# Load .env keys
load_dotenv()

# Fetch API keys from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# --------------- Function Definitions ----------------

def get_name(_input=""):
    return "My name is Gursimran Kaur."

def get_quote(_input=""):
    return "Success is not final, failure is not fatal: It is the courage to continue that counts. — Winston Churchill"

def get_health_tip(_input=""):
    return "Stay hydrated, exercise regularly, get 7-8 hours of sleep, and avoid junk food."

def get_weather(city_name: str):
    """Returns real-time weather for the given city."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city_name}&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return f"❌ Error: {data['error']['message']}"

        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]

        return f"📍 {city_name.title()} | Temperature: {temp}°C | Condition: {condition} | Humidity: {humidity}%"
    except Exception as e:
        return f"❌ Failed to get weather: {str(e)}"

# ----------------- LangChain Tools -----------------

tools = [
    Tool.from_function(
        func=get_name,
        name="NameTool",
        description="Returns the name of the user."
    ),
    Tool.from_function(
        func=get_quote,
        name="QuotesTool",
        description="Provides a motivational quote."
    ),
    Tool.from_function(
        func=get_health_tip,
        name="HealthTipsTool",
        description="Provides general health tips."
    ),
    Tool.from_function(
        func=get_weather,
        name="WeatherTool",
        description="Provides real-time weather. Input should be a city name like 'Mumbai' or 'Delhi'."
    )
]

# ----------------- Gemini LLM Setup -----------------

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY,
    verbose=True
)

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ----------------- CLI Interaction -----------------

print("\n🧠 Gemini Function Calling Agent Ready!")
while True:
    user_input = input("\n💬 Ask something (or type 'exit'): ")
    if user_input.lower() == "exit":
        print("👋 Exiting...")
        break

    result = agent_executor.run(user_input)
    print(f"\n📩 Response: {result}")