import tkinter as tk
from tkinter import ttk
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import threading
import numpy as np
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ✅ Hugging Face API Key
API_KEY = ""

# Globals
is_recording = False
is_paused = False
recording_thread = None
recorded_chunks = []
samplerate = 16000
chunk_duration = 8
fixed_duration = 30
total_chunk_time = 60

# === Whisper API ===
def transcribe_audio_with_whisper(audio_file):
    url = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "audio/wav"
    }
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    response = requests.post(url, headers=headers, data=audio_bytes)
    if response.status_code == 200:
        result = response.json()
        return result.get("text", "[No transcription returned]")
    else:
        return f"❌ Error {response.status_code}: {response.text}"

def save_audio_to_file(filename="output.wav"):
    full_audio = np.concatenate(recorded_chunks, axis=0)
    write(filename, samplerate, full_audio)
    return filename

def update_waveform(data):
    if len(data) > 0:
        y_data = data.flatten()
        x_data = np.arange(len(y_data))
        line.set_data(x_data, y_data)
        ax.set_xlim(0, len(y_data))
        canvas.draw()

def record_audio_chunked():
    global is_recording, is_paused, recorded_chunks
    recorded_chunks = []
    total_recorded = 0
    while is_recording and total_recorded < total_chunk_time:
        if not is_paused:
            remaining = total_chunk_time - total_recorded
            duration = min(chunk_duration, remaining)
            audio_chunk = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
            sd.wait()
            recorded_chunks.append(audio_chunk)
            update_waveform(audio_chunk)
            total_recorded += duration
        else:
            time.sleep(1)
            is_recording = False
            filename = save_audio_to_file()
            status_label.config(text="✅ Saved as output.wav")
            transcription = transcribe_audio_with_whisper(filename)
            transcription_box.delete(1.0, tk.END)
            transcription_box.insert(tk.END, transcription)
            num_words = len(transcription.strip().split())
            duration_sec = len(np.concatenate(recorded_chunks)) / samplerate
            stats_label.config(text=f"📊 Words: {num_words} | Duration: {round(duration_sec, 2)} sec")


def record_audio_fixed():
    global is_recording, recorded_chunks
    recorded_chunks = []
    audio = sd.rec(int(fixed_duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    recorded_chunks.append(audio)
    is_recording = False
    update_waveform(audio)
    filename = save_audio_to_file()
    status_label.config(text="✅ Saved as output.wav")
    transcription = transcribe_audio_with_whisper(filename)
    transcription_box.delete(1.0, tk.END)
    transcription_box.insert(tk.END, transcription)
    num_words = len(transcription.strip().split())
    duration_sec = len(np.concatenate(recorded_chunks)) / samplerate
    stats_label.config(text=f"📊 Words: {num_words} | Duration: {round(duration_sec, 2)} sec")

# === Button Actions ===
def start_chunked_recording():
    global is_recording, recording_thread
    is_recording = True
    is_paused = False
    recording_thread = threading.Thread(target=record_audio_chunked)
    recording_thread.start()
    status_label.config(text="🔴 Recording with breaks...")

def start_fixed_recording():
    global is_recording, recording_thread
    is_recording = True
    recording_thread = threading.Thread(target=record_audio_fixed)
    recording_thread.start()
    status_label.config(text="🔴 Recording fixed duration...")

def pause_recording():
    global is_paused
    is_paused = True
    status_label.config(text="⏸️ Paused")

def resume_recording():
    global is_paused
    is_paused = False
    status_label.config(text="🔴 Resumed recording...")

def stop_recording():
    global is_recording
    is_recording = False
    if recording_thread:
        recording_thread.join()
    if recorded_chunks:
        filename = save_audio_to_file()
        transcription = transcribe_audio_with_whisper(filename)
        transcription_box.delete(1.0, tk.END)
        transcription_box.insert(tk.END, transcription)
        num_words = len(transcription.strip().split())
        duration_sec = len(np.concatenate(recorded_chunks)) / samplerate
        stats_label.config(text=f"📊 Words: {num_words} | Duration: {round(duration_sec, 2)} sec")
        status_label.config(text="✅ Recording manually stopped and transcribed")

def update_timing():
    global chunk_duration, fixed_duration, total_chunk_time
    try:
        chunk_duration = int(chunk_entry.get())
        total_chunk_time = int(total_chunk_entry.get())
        fixed_duration = int(fixed_entry.get())
        status_label.config(text=f"⏱️ Timings updated")
    except ValueError:
        status_label.config(text="❌ Invalid time entered!")

# === GUI Setup ===
app = tk.Tk()
app.title("🎤 Whisper Speech-to-Text Interface")
app.geometry("800x700")
app.config(bg="#f6c78a")

navbar = tk.Frame(app, bg="#d48d47", height=60)
navbar.pack(fill=tk.X)
nav_title = tk.Label(navbar, text="🎧 Whisper Recorder", bg="#d48d47", fg="white", font=("Helvetica", 18, "bold"))
nav_title.pack(pady=10)

mode_frame = tk.Frame(app, bg="#f6c78a")
mode_frame.pack(pady=10)

tk.Label(mode_frame, text="Chunk Duration (sec):", bg="#f6c78a").grid(row=0, column=0, padx=5)
chunk_entry = tk.Entry(mode_frame, width=5)
chunk_entry.insert(0, "8")
chunk_entry.grid(row=0, column=1, padx=5)

tk.Label(mode_frame, text="Total Chunk Time (sec):", bg="#f6c78a").grid(row=0, column=2, padx=5)
total_chunk_entry = tk.Entry(mode_frame, width=5)
total_chunk_entry.insert(0, "60")
total_chunk_entry.grid(row=0, column=3, padx=5)

tk.Label(mode_frame, text="Fixed Duration (sec):", bg="#f6c78a").grid(row=0, column=4, padx=5)
fixed_entry = tk.Entry(mode_frame, width=5)
fixed_entry.insert(0, "30")
fixed_entry.grid(row=0, column=5, padx=5)

ttk.Button(mode_frame, text="Set Timings", command=update_timing).grid(row=0, column=6, padx=10)

buttons_frame = tk.Frame(app, bg="#f6c78a")
buttons_frame.pack(pady=20)

ttk.Button(buttons_frame, text="🎤 Start Chunked", command=start_chunked_recording).grid(row=0, column=0, padx=10)
ttk.Button(buttons_frame, text="🎙️ Start Fixed", command=start_fixed_recording).grid(row=0, column=1, padx=10)
ttk.Button(buttons_frame, text="⏸️ Pause", command=pause_recording).grid(row=0, column=2, padx=10)
ttk.Button(buttons_frame, text="⏯️ Resume", command=resume_recording).grid(row=0, column=3, padx=10)
ttk.Button(buttons_frame, text="⏹️ Stop & Transcribe", command=stop_recording).grid(row=0, column=4, padx=10)

status_label = tk.Label(app, text="🟡 Waiting...", bg="#f6c78a", font=("Arial", 12))
status_label.pack(pady=10)

transcription_box = tk.Text(app, height=10, width=90, wrap="word", font=("Courier", 11))
transcription_box.pack(pady=10)

plot_frame = tk.Frame(app, bg="#f6c78a")
plot_frame.pack(pady=5)

fig = Figure(figsize=(7, 2), dpi=100)
ax = fig.add_subplot(111)
ax.set_ylim([-30000, 30000])
ax.set_title("🎵 Live Waveform")
line, = ax.plot([], [], lw=1)

canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack()

stats_label = tk.Label(app, text="📊 Stats: --", bg="#f6c78a", font=("Arial", 11))
stats_label.pack(pady=10)

app.mainloop()