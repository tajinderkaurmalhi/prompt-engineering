import os
import platform
import subprocess
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import requests
import google.generativeai as genai

# === CONFIG ===
GOOGLE_API_KEY = "AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA"
ELEVEN_API_KEY = "sk_dc6b438812ec90343cf5e78d78ed616858a342c2597a708e"
DURATION = 6
counter = 1
voice_id = None

# === Setup Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Play audio file (cross-platform)
def play_audio_file(filepath):
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(filepath)
        elif system == "Darwin":  # macOS
            subprocess.call(["afplay", filepath])
        elif system == "Linux":
            subprocess.call(["xdg-open", filepath])
        else:
            print("⚠️ Unsupported OS for audio playback.")
    except Exception as e:
        print(f"❌ Error playing audio: {e}")

# === Get Default ElevenLabs Voice
def get_default_voice():
    response = requests.get("https://api.elevenlabs.io/v1/voices", headers={
        "xi-api-key": ELEVEN_API_KEY
    })
    if response.status_code == 200:
        voices = response.json()["voices"]
        return voices[0]["voice_id"]
    else:
        print("❌ Could not fetch voices.")
        exit()

# === Record Audio from Mic
def record_audio(filename):
    print("🎤 Speak now...")
    audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    write(filename, SAMPLERATE, audio)
    print(f"✅ Audio saved to: {filename}")

# === Transcribe Using Google Speech Recognition
def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You asked: {text}")
        return text
    except Exception as e:
        print(f"❌ Could not transcribe: {e}")
        return ""

# === Generate Answer using Gemini Flash
def get_gemini_reply(prompt):
    print("🤖 Generating reply using Gemini Flash...")
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    answer = response.text
    print(f"🤖 AI says: {answer}")
    return answer

# === Convert Text to Speech with ElevenLabs
def text_to_speech(text, filename, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Voice reply saved as: {filename}")
    else:
        print(f"❌ ElevenLabs Error: {response.text}")

# === Main Voice-to-Voice Loop
def run_bot():
    global counter, voice_id
    print("\n🎙️ Voice-to-Voice Assistant (Gemini Flash + ElevenLabs)")

    if voice_id is None:
        voice_id = get_default_voice()

    while True:
        cmd = input("\n▶️ Press Enter to ask or type 'exit': ")
        if cmd.lower() == "exit":
            print("👋 Exiting the assistant.")
            break

        user_audio = f"user_audio_{counter}.wav"
        ai_audio = f"ai_reply_{counter}.mp3"

        # 1. Record User Audio
        record_audio(user_audio)

        # 2. Transcribe Audio
        question = transcribe_audio(user_audio)
        if not question.strip():
            continue

        # 3. Get AI Response from Gemini
        answer = get_gemini_reply(question)

        # 4. Convert Answer to Voice
        text_to_speech(answer, ai_audio, voice_id)

        # ✅ 5. Play the Audio Output in Terminal
        play_audio_file(ai_audio)

        counter += 1

# === Run the Bot
if __name__ == "__main__":
    run_bot()