import customtkinter as ctk
import threading
import time
import sounddevice as sd
import numpy as np
import queue
import webrtcvad
import collections
import pyttsx3
import noisereduce as nr
from faster_whisper import WhisperModel
from transformers import MarianMTModel, MarianTokenizer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ==========================
# CONFIGURATION
# ==========================
SAMPLE_RATE = 16000
FRAME_DURATION = 30
VAD_MODE = 2
SILENCE_TIMEOUT = 1.0

LANGUAGES = {
    "🇮🇳 Hindi": "Helsinki-NLP/opus-mt-en-hi",
    "🇩🇪 German": "Helsinki-NLP/opus-mt-en-de",
    "🇫🇷 French": "Helsinki-NLP/opus-mt-en-fr",
    "🇪🇸 Spanish": "Helsinki-NLP/opus-mt-en-es",
}

# ==========================
# MODELS
# ==========================
print("Loading Whisper...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 170)

vad = webrtcvad.Vad(VAD_MODE)
audio_queue = queue.Queue()

translator = None
tokenizer = None
running = False

# ==========================
# GUI SETUP
# ==========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🌍 Offline Real-Time Voice Translator")
app.geometry("1000x750")

# ==========================
# HEADER
# ==========================
title = ctk.CTkLabel(
    app,
    text="🌍 Offline Voice Translator",
    font=("Segoe UI", 28, "bold")
)
title.pack(pady=20)

# ==========================
# TOP CONTROLS
# ==========================
control_frame = ctk.CTkFrame(app)
control_frame.pack(fill="x", padx=20, pady=10)

target_lang = ctk.StringVar(value="🇮🇳 Hindi")

lang_dropdown = ctk.CTkComboBox(
    control_frame,
    values=list(LANGUAGES.keys()),
    variable=target_lang,
    width=200
)
lang_dropdown.pack(side="left", padx=10)

status_label = ctk.CTkLabel(control_frame, text="Status: Idle")
status_label.pack(side="left", padx=20)

latency_label = ctk.CTkLabel(control_frame, text="Latency: - ms")
latency_label.pack(side="left", padx=20)

# Light/Dark Toggle
def toggle_theme():
    mode = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if mode == "Dark" else "dark")

theme_btn = ctk.CTkButton(control_frame, text="🌗 Toggle Theme", command=toggle_theme)
theme_btn.pack(side="right", padx=10)

# ==========================
# TEXT DISPLAY
# ==========================
recognized_box = ctk.CTkTextbox(app, height=120)
recognized_box.pack(fill="x", padx=20, pady=10)

translated_box = ctk.CTkTextbox(app, height=120)
translated_box.pack(fill="x", padx=20, pady=10)

# ==========================
# WAVEFORM
# ==========================
fig = Figure(figsize=(8, 2), dpi=100)
ax = fig.add_subplot(111)
ax.set_ylim(-1, 1)
ax.set_xlim(0, 1000)
line, = ax.plot([], [])

canvas = FigureCanvasTkAgg(fig, master=app)
canvas.get_tk_widget().pack(fill="x", padx=20)

# ==========================
# BUTTONS
# ==========================
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

def start():
    global running
    if not running:
        load_translator()
        running = True
        status_label.configure(text="Status: Listening 🟢")
        threading.Thread(target=stream_translator, daemon=True).start()

def stop():
    global running
    running = False
    status_label.configure(text="Status: Stopped 🔴")

start_btn = ctk.CTkButton(button_frame, text="▶ Start", command=start, width=150)
start_btn.pack(side="left", padx=20)

stop_btn = ctk.CTkButton(button_frame, text="⏹ Stop", command=stop, width=150)
stop_btn.pack(side="left", padx=20)

# ==========================
# AUDIO CALLBACK
# ==========================
def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())
    update_waveform(indata.flatten())

def update_waveform(data):
    line.set_data(range(len(data)), data)
    ax.set_xlim(0, len(data))
    canvas.draw_idle()

# ==========================
# TRANSLATOR LOADER
# ==========================
def load_translator():
    global translator, tokenizer
    model_name = LANGUAGES[target_lang.get()]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    translator = MarianMTModel.from_pretrained(model_name)

# ==========================
# NOISE REDUCTION
# ==========================
def reduce_noise(audio):
    return nr.reduce_noise(y=audio, sr=SAMPLE_RATE)

# ==========================
# TYPING EFFECT
# ==========================
def type_text(widget, text):
    widget.delete("0.0", "end")
    for char in text:
        widget.insert("end", char)
        widget.update()
        time.sleep(0.01)

# ==========================
# STREAM THREAD
# ==========================
def stream_translator():
    global running

    ring_buffer = collections.deque(maxlen=int(SILENCE_TIMEOUT * 1000 / FRAME_DURATION))
    triggered = False
    voiced_frames = []

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        blocksize=int(SAMPLE_RATE * FRAME_DURATION / 1000),
        callback=audio_callback
    ):
        while running:
            frame = audio_queue.get()
            pcm_data = (frame * 32768).astype(np.int16).tobytes()
            is_speech = vad.is_speech(pcm_data, SAMPLE_RATE)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                if sum(1 for f, s in ring_buffer if s) > 0.9 * ring_buffer.maxlen:
                    triggered = True
                    voiced_frames.extend([f for f, s in ring_buffer])
                    ring_buffer.clear()
            else:
                voiced_frames.append(frame)
                ring_buffer.append((frame, is_speech))

                if sum(1 for f, s in ring_buffer if not s) > 0.9 * ring_buffer.maxlen:
                    triggered = False

                    start_time = time.time()

                    audio_data = np.concatenate(voiced_frames, axis=0)
                    audio_data = np.squeeze(audio_data)
                    audio_data = reduce_noise(audio_data)

                    segments, info = whisper_model.transcribe(audio_data)
                    text = " ".join([seg.text for seg in segments])

                    if text.strip():
                        type_text(recognized_box, text)

                        inputs = tokenizer(text, return_tensors="pt", padding=True)
                        translated = translator.generate(**inputs)
                        translated_text = tokenizer.decode(
                            translated[0], skip_special_tokens=True
                        )

                        type_text(translated_box, translated_text)

                        tts_engine.say(translated_text)
                        tts_engine.runAndWait()

                        latency = int((time.time() - start_time) * 1000)
                        latency_label.configure(text=f"Latency: {latency} ms")

                    ring_buffer.clear()
                    voiced_frames = []

app.mainloop()
