import requests
import random
import string
import time

# ✅ Your ElevenLabs API Key
API_KEY = "sk_dc6b438812ec90343cf5e78d78ed616858a342c2597a708e"

# ✅ ElevenLabs Endpoint
BASE_URL = "https://api.elevenlabs.io/v1"
HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

# ✅ Get Default Voice ID
def get_default_voice_id():
    response = requests.get(f"{BASE_URL}/voices", headers=HEADERS)
    if response.status_code == 200:
        voices = response.json()["voices"]
        if voices:
            return voices[0]["voice_id"]
        else:
            print("❌ No voices found.")
            exit()
    else:
        print(f"❌ Error fetching voices: {response.text}")
        exit()

# ✅ Save response audio
def save_audio(content, filename):
    with open(filename, 'wb') as f:
        f.write(content)

# ✅ Generate random filename
def random_filename(prefix="reply_", ext=".mp3"):
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}{rand}{ext}"

# ✅ Speak with ElevenLabs API
def speak_with_elevenlabs(text, voice_id):
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(f"{BASE_URL}/text-to-speech/{voice_id}", headers=HEADERS, json=payload)

    if response.status_code == 200:
        filename = random_filename()
        save_audio(response.content, filename)
        print(f"✅ Audio saved as: {filename}")
        return filename
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None

# ✅ Main Bot Loop
def run_text_to_speech_bot():
    print("🎙️ Text to Speech Bot using ElevenLabs")
    voice_id = get_default_voice_id()

    while True:
        user_input = input("\n📝 Enter your text (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("👋 Exiting...")
            break

        print(f"\n📣 You said: {user_input}")
        print("🔁 Generating voice...")

        filename = speak_with_elevenlabs(user_input, voice_id)

        if filename:
            print(f"🔊 Playing AI response: {filename}\n")
            # Optional: Play the file if on Windows/Linux/macOS
            try:
                import platform, os
                if platform.system() == "Darwin":  # macOS
                    os.system(f"afplay {filename}")
                elif platform.system() == "Windows":
                    os.system(f"start {filename}")
                else:  # Linux
                    os.system(f"mpg123 {filename}")
            except:
                print("🔇 Unable to auto-play audio on this system.")

# ✅ Run the bot
if __name__ == "__main__":
    run_text_to_speech_bot()