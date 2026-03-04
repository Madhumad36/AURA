# AURA

AURA is a simple real-time assistive audio pipeline in Python.  
It listens to microphone audio, detects speech activity, classifies ambient sound, decides when to speak, and provides voice feedback.

## Project Structure

- `orchestrator/aura_core.py`: Main runtime loop that connects all modules.
- `audio_capture/mic_stream.py`: Captures real-time microphone audio.
- `vad/vad_engine.py`: Voice activity detection using `webrtcvad`.
- `audio_classification/ambient_classifier.py`: Ambient sound classification using YAMNet (`tensorflow_hub`).
- `decision_engine/rule_engine.py`: Rule logic for when AURA should speak.
- `output/tts.py`: Text-to-speech output using `pyttsx3`.
- `audio_preprocessing/preprocess.py`: Log-Mel feature extraction helpers.
- `test_vad.py`, `test_tts.py`, `test_rule_engine.py`: Simple module test scripts.

## Requirements

This project uses Python 3.11+ and common audio/ML libraries:

- `numpy`
- `sounddevice`
- `webrtcvad`
- `tensorflow`
- `tensorflow-hub`
- `librosa`
- `pyttsx3`



## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install numpy sounddevice webrtcvad tensorflow tensorflow-hub librosa pyttsx3
```

## Run AURA

```bash
python orchestrator/aura_core.py
```

## Run Individual Tests

```bash
python test_vad.py
python test_tts.py
python test_rule_engine.py
```

## Notes

- Press `Ctrl+C` to stop real-time scripts.
- Microphone access is required.
- First run of the ambient classifier may download model assets.
