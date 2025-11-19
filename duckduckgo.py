import requests
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType

# 🔐 API Keys
GOOGLE_API_KEY = "AIzaSyA-WsjPebJfmXZst8FUdgeWOELt2hYcdSE"
WEATHER_API_KEY = "a4018011b06f4fe68ed82513251607"

# ------------------ Tool Functions ------------------

def get_name():
    return "My name is Gursimran Kaur."

def get_quote():
    return "Success is not final, failure is not fatal: It is the courage to continue that counts. — Winston Churchill"

def get_health_tips():
    return "Stay hydrated, exercise regularly, get 7-8 hours of sleep, and avoid junk food."

def get_weather(city: str):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return f"❌ Error: {data['error']['message']}"

        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']

        # ✅ Avoid repeating trigger words like "weather"
        return f"{city} is currently {temp_c}°C with {condition}. Humidity is {humidity}%."
    except Exception as e:
        return f"❌ Failed to fetch weather: {str(e)}"

# ------------------ Tools List ------------------

tools = [
    Tool(
        name="NameTool",
        func=lambda _: get_name(),
        description="Tells the name of the user.",
        return_direct=True
    ),
    Tool(
        name="QuotesTool",
        func=lambda _: get_quote(),
        description="Provides inspirational quotes.",
        return_direct=True
    ),
    Tool(
        name="HealthTipsTool",
        func=lambda _: get_health_tips(),
        description="Gives useful health tips.",
        return_direct=True
    ),
    Tool(
        name="WeatherTool",
        func=lambda city: get_weather(city),
        description="Gives real-time weather. Input should be a city name like 'Delhi'.",
        return_direct=True
    ),
]

# ------------------ LLM & Agent Setup ------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY,
    verbose=False  # LLM internal logs off
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  # ✅ Show Thought → Action → Result flow
)

# ------------------ Interaction Loop ------------------

if __name__ == "__main__":
    print("🤖 Ask me:\n- 'What's your name?'\n- 'Give me a quote'\n- 'Weather Delhi'\n- 'Health tip'\nOr anything general.\n")

    while True:
        user_input = input("📝 You: ")
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break

        result = agent.run(user_input)
        print("📩", result)