# AURA Setup Guide

## Prerequisites

Before running the project, ensure the following software is installed:

- Python 3.10 or later
- Visual Studio Code
- Git (optional)
- Working microphone
- Internet connection (required for some text-to-speech operations)

---

# Project Structure

AURA/
│
├── audio_capture/
├── audio_classification/
├── decision_engine/
├── output/
├── utils/
├── vad/
├── vision_module/
├── logs/
├── app.py
├── requirements.txt
└── README.md

---

# Step 1: Create Virtual Environment

Open terminal inside the project directory.

```bash
python -m venv aura_env
```

Activate environment:

### Windows

```bash
aura_env\Scripts\activate
```

### Linux / Mac

```bash
source aura_env/bin/activate
```

---

# Step 2: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

If requirements.txt is unavailable, install manually:

```bash
pip install streamlit
pip install ultralytics
pip install transformers
pip install torch
pip install torchvision
pip install opencv-python
pip install pandas
pip install numpy
pip install pyaudio
pip install pyttsx3
pip install webrtcvad
pip install pillow
pip install gtts
```

---

# Step 3: Verify Installation

Check Python version:

```bash
python --version
```

Verify important libraries:

```bash
python -c "import cv2"
python -c "from ultralytics import YOLO"
python -c "from transformers import BlipProcessor"
python -c "import streamlit"
```

No errors indicate successful installation.

---

# Running the Audio Module

Navigate to the project root directory and execute:

```bash
python orchestrator/aura_core.py
```

The audio module will:

- Capture microphone input
- Perform Voice Activity Detection (VAD)
- Classify environmental sounds
- Generate contextual interpretations
- Produce speech feedback
- Save logs for analysis

---

# Running the Vision Module

Execute:

```bash
python vision_module/vision_core.py
```

The vision module will:

- Accept video input
- Extract frames
- Perform YOLO object detection
- Generate BLIP captions
- Create scene interpretations
- Produce analysis outputs

---

# Running the Streamlit Interface

Launch the integrated interface:

```bash
streamlit run app.py
```

After execution, Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open the URL in a web browser.

---

# Using Audio Analysis

1. Select "Audio Analysis" mode.
2. Choose recording duration.
3. Click "Start Analysis".
4. Allow microphone access if prompted.
5. Wait until processing completes.
6. Review logs, metrics, and graphs.

---

# Using Vision Analysis

1. Select "Vision Analysis" mode.
2. Upload a supported video file.
3. Click "Run Analysis".
4. Wait for processing to finish.
5. Review:
   - Scene Interpretation
   - Detection Data
   - System Confidence
   - Activity Analysis Graphs
   - Speech Output

---

# Generated Outputs

## Audio Module

Generated files may include:

```text
logs/
└── aura_logs.csv
```

Outputs:

- Environmental labels
- Confidence values
- VAD status
- Graphical analytics

---

## Vision Module

Generated files may include:

```text
vision_analysis.csv
output.mp3
```

Outputs:

- Object detections
- Scene interpretations
- Confidence indicators
- Speech narration
- Activity graphs

---

# Common Issues

## Microphone Not Detected

Verify:

- Microphone permissions are enabled
- Correct recording device is selected
- Audio drivers are installed

---

## Streamlit Not Opening

Run:

```bash
streamlit run app.py
```

If issue persists:

```bash
pip install --upgrade streamlit
```

---

## YOLO Model Download Error

Ensure internet connectivity during first execution.

YOLO weights are downloaded automatically on first run.

---

## PyAudio Installation Error

For Windows:

```bash
pip install pipwin
pipwin install pyaudio
```

---

# System Requirements

Minimum:

- Intel i5 Processor
- 8 GB RAM
- Windows 10/11
- Python 3.10+

Recommended:

- Intel i7 Processor
- 16 GB RAM
- Dedicated GPU (optional)
- SSD Storage

---

# Successful Setup Checklist

✓ Python Installed

✓ Virtual Environment Created

✓ Dependencies Installed

✓ Audio Module Running

✓ Vision Module Running

✓ Streamlit Interface Accessible

✓ Logs Generated Successfully

✓ Graphs and Outputs Displayed Correctly

The AURA system is now ready for execution and demonstration.
