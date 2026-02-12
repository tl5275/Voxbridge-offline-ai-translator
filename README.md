# 🌍 VoxBridge – Offline AI Voice Translator

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Offline AI](https://img.shields.io/badge/AI-Fully%20Offline-green)
![Edge Ready](https://img.shields.io/badge/Edge-Deployable-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

🚀 A fully offline, real-time multilingual AI voice translator with modern GUI, automatic language detection, silence-aware processing, and noise robustness.

---

## 🧠 Problem Statement

Most real-time translation systems rely on cloud APIs. In rural areas, disaster zones, defense operations, and low-connectivity environments, internet-based solutions fail.

We built a **fully offline AI-powered voice translator** that works in real-time without internet access.

---

## 💡 Our Solution

VoxBridge enables:

- 🎤 Real-time speech capture
- 🔇 Silence-aware sentence processing
- 🧠 Automatic language detection
- 🌍 Neural machine translation
- 🔊 Offline speech synthesis
- 🎨 Modern, production-level GUI

All running locally on CPU.

---

## ✨ Key Features

### 🎛 Multi-Language Target Selection
- 🇮🇳 Hindi
- 🇩🇪 German
- 🇫🇷 French
- 🇪🇸 Spanish
- Easily extendable

### 🧠 Automatic Language Detection
User can speak in any supported language.
Whisper auto-detects input language.

### 🔇 Silence Detection
Processes speech only after silence (Google Translate style).

### 🎤 Noise Robustness
- Spectral noise reduction
- WebRTC Voice Activity Detection
- Stable performance in noisy environments

### 🎨 Modern GUI
- 🌙 Dark / Light toggle
- 📦 Framed layout
- 🎛 Styled rounded buttons
- 📊 Latency display
- 🔵 Live waveform visualization
- 🟣 Real-time typing animation
- 🟢 Listening indicator

### 🔊 Fully Offline
No cloud APIs. No internet required after initial model download.

---

## 🏗 System Architecture

Microphone  
↓  
WebRTC VAD (Silence Detection)  
↓  
Noise Reduction  
↓  
Faster-Whisper (Auto Language Detection + STT)  
↓  
MarianMT Neural Translation  
↓  
Offline Text-to-Speech  
↓  
Modern GUI  

### 📊 Architecture Diagram

![Architecture](assets/architecture.png)

---

## ⚙ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/tl5275/voxbridge-offline-ai-translator.git
cd voxbridge-offline-ai-translator
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install FFmpeg

Windows:
Download from https://www.gyan.dev/ffmpeg/builds/

Mac:
```bash
brew install ffmpeg
```

---

## ▶ Run Application

```bash
python main.py
```

Select target language.
Click Start.
Speak naturally.
Translation will occur after silence.

---

## 🖥 Application Preview

### 🌙 Dark Mode
![Dark Mode](assets/screenshots/dark_mode.png)

### ☀ Light Mode
![Light Mode](assets/screenshots/light_mode.png)

---

## 📊 Performance

| Stage | Avg Latency |
|-------|------------|
| Speech Recognition | 300–800 ms |
| Translation | 200–400 ms |
| End-to-End | ~1 second |

CPU-based execution. No GPU required.

---

## 🎯 Use Cases

- Rural healthcare communication
- Disaster response systems
- Defense field deployment
- Travel translation device
- Accessibility technology
- Edge AI applications

---

## 🧠 Technologies Used

- Faster-Whisper
- MarianMT (Helsinki-NLP)
- WebRTC VAD
- Noisereduce
- CustomTkinter
- Matplotlib
- PyTorch

---

## 🏆 Value Proposition

✔ Fully Offline AI  
✔ Real-Time Processing  
✔ Edge Deployable  
✔ No Cloud Dependency  
✔ Production-Level GUI  
✔ Scalable Architecture  

---

## 📜 License

MIT License
