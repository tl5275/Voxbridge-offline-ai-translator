# System Design – VoxBridge

## Overview

VoxBridge is a fully offline, real-time AI voice translator designed for edge environments with no internet dependency.

## Core Processing Pipeline

1. Audio Capture (sounddevice)
2. Voice Activity Detection (WebRTC VAD)
3. Noise Reduction (Spectral Filtering)
4. Speech-to-Text (Faster-Whisper)
5. Automatic Language Detection
6. Neural Machine Translation (MarianMT)
7. Offline Text-to-Speech (pyttsx3)
8. GUI Rendering (CustomTkinter)

## Optimization Techniques

- INT8 quantization for faster inference
- Silence-aware buffering to reduce compute load
- CPU-only execution (no GPU required)
- Model preloading to reduce runtime latency
- Modular architecture for scalability

## Deployment Target

- Windows
- macOS (Apple Silicon compatible)
- Edge deployment possible
