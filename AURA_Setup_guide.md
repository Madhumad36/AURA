

```
AURA_SETUP_GUIDE.md
```


---

# AURA – AI-Powered Social Context Awareness System

### A Digital Sixth Sense for the Visually Impaired

---

# 1. Project Overview

AURA is a **real-time assistive system** designed to provide **social and environmental awareness** to visually impaired individuals.

The system continuously listens to the surrounding environment using a microphone and analyzes ambient audio using machine learning models. Based on detected environmental context, AURA provides **audio feedback through text-to-speech** to inform the user about their surroundings.

The system works fully in **real-time** and processes audio locally on the device.

Example outputs:

```
"The environment is quiet."
"People are having conversations nearby."
"The environment is noisy."
```

---

# 2. Core Idea

Visually impaired individuals often struggle to understand **social context**, such as:

* whether people are talking nearby
* whether the environment is crowded
* whether it is quiet or noisy

AURA acts as a **digital sixth sense** by analyzing environmental audio and providing spoken feedback.

---

# 3. System Architecture

AURA is built using a **modular pipeline architecture**.

```
Microphone Input
        ↓
Audio Capture Module
        ↓
Voice Activity Detection (VAD)
        ↓
Audio Classification (YAMNet)
        ↓
Environment Mapping
        ↓
Decision Engine
        ↓
Text-To-Speech Output
```

---

# 4. Folder Structure

Project directory structure:

```
AURA/
│
├── audio_capture/
│   ├── __init__.py
│   └── mic_stream.py
│
├── audio_preprocessing/
│   ├── __init__.py
│   └── preprocess.py
│
├── audio_classification/
│   ├── __init__.py
│   └── ambient_classifier.py
│
├── vad/
│   ├── __init__.py
│   └── vad_engine.py
│
├── decision_engine/
│   ├── __init__.py
│   └── rule_engine.py
│
├── output/
│   ├── __init__.py
│   └── tts.py
│
├── orchestrator/
│   ├── __init__.py
│   └── aura_core.py
│
├── test_vad.py
├── test_tts.py
├── test_rule_engine.py
│
└── README.md
```

---

# 5. Development Environment

The project was developed and tested with the following environment.

### Python Version

```
Python 3.11.9
```

Python 3.11 is used because some libraries (especially `webrtcvad`) are not fully compatible with Python 3.13.

---

# 6. Required Hardware

Minimum requirements:

* Microphone (built-in laptop microphone is sufficient)
* Laptop / PC
* Internet connection (first run downloads YAMNet model)

Optional:

* External microphone for better detection

---

# 7. Required Python Libraries

AURA depends on the following libraries:

```
tensorflow
tensorflow-hub
numpy
sounddevice
librosa
scikit-learn
webrtcvad
pyttsx3
```

Additional dependencies automatically installed:

```
scipy
numba
joblib
pooch
tensorboard
```

---

# 8. Installing the Project

## Step 1 – Clone or Download the Project

Example:

```
git clone <repository link>
```

Or download the ZIP file and extract it.

Navigate to project directory:

```
cd AURA
```

---

# 9. Creating a Virtual Environment

Creating a virtual environment is **strongly recommended**.

It prevents conflicts with other Python projects.

### Create virtual environment

Windows:

```
python -m venv .venv
```

---

### Activate virtual environment

Windows PowerShell:

```
.venv\Scripts\Activate.ps1
```

After activation you should see:

```
(.venv)
```

before the terminal prompt.

---

# 10. Installing Dependencies

Run the following command:

```
pip install tensorflow tensorflow-hub numpy sounddevice librosa scikit-learn webrtcvad pyttsx3
```

This may take a few minutes because TensorFlow is large.

---

# 11. First Time Model Download

When running the classifier for the first time:

TensorFlow Hub automatically downloads the **YAMNet model**.

```
https://tfhub.dev/google/yamnet/1
```

The model is cached locally after the first run.

---

# 12. Running Individual Components

Before running the full system, individual modules can be tested.

---

# 12.1 Testing Microphone Stream

Run:

```
python -m audio_capture.mic_stream
```

Expected output:

```
Captured audio frame: (16000,)
Captured audio frame: (16000,)
```

Each frame represents **1 second of audio at 16kHz**.

---

# 12.2 Testing Voice Activity Detection

Run:

```
python test_vad.py
```

Expected output:

```
Speech Detected: False
Speech Detected: False
Speech Detected: True
Speech Detected: True
```

This detects whether human speech is present in the audio.

---

# 12.3 Testing Text-To-Speech

Run:

```
python test_tts.py
```

Expected output:

The system speaks:

```
"This is AURA testing speech output."
```

---

# 12.4 Testing Rule Engine

Run:

```
python test_rule_engine.py
```

Expected output:

```
AURA would say: The environment is quiet.
AURA would say: People are having conversations nearby.
```

This verifies that the decision logic works correctly.

---

# 12.5 Testing Ambient Environment Classifier

Run:

```
python -m audio_classification.ambient_classifier
```

Expected output:

```
Detected Environment: conversational
Confidence: 0.87
```

Possible labels:

```
quiet
conversational
noisy
crowded
```

---

# 13. Running the Complete AURA System

To run the full system pipeline:

```
python -m orchestrator.aura_core
```

Example output:

```
AURA – Real Time Assistive System

AURA says: The environment is conversational.
AURA says: The environment is quiet.
```

The system continuously listens to environmental audio.

---

# 14. How the System Works Internally

Each second the system performs the following pipeline.

### Step 1 – Audio Capture

```
mic_stream.py
```

Captures **1 second audio chunks (16000 samples)**.

---

### Step 2 – Voice Activity Detection

```
vad_engine.py
```

Determines whether someone is speaking.

This prevents AURA from speaking over a conversation.

---

### Step 3 – Ambient Audio Classification

```
ambient_classifier.py
```

Uses **Google YAMNet model**.

YAMNet detects **521 different audio classes**.

These are mapped to simplified environments:

```
speech → conversational
crowd/applause → crowded
traffic/engine → noisy
else → quiet
```

---

### Step 4 – Temporal Smoothing

To prevent unstable predictions:

```
2 consecutive predictions required
```

before changing environment state.

This improves stability.

---

### Step 5 – Decision Engine

```
rule_engine.py
```

Controls when AURA should speak.

Rules include:

* minimum confidence threshold
* cooldown between announcements
* avoid interrupting speech

---

### Step 6 – Text-To-Speech Output

```
tts.py
```

Converts messages into spoken audio.

Example messages:

```
"The environment is quiet."
"People are having conversations nearby."
```

---

# 15. Key System Parameters

These can be tuned:

### Classification Confidence

```
confidence_threshold = 0.4
```

---

### Temporal Smoothing

```
smoothing_window = 2
```

---

### Announcement Cooldown

```
cooldown_seconds = 20
```

Prevents repeated announcements.

---

# 16. Example Use Case

User enters a room where people are talking.

Pipeline behavior:

```
audio detected
↓
speech detected
↓
environment classified as conversational
↓
rule engine triggers
↓
AURA says:
"People are having conversations nearby."
```

---

# 17. Limitations

Current limitations:

* audio-only system
* limited environment classes
* occasional classification noise
* depends on microphone quality

---

# 18. Future Improvements

Future versions may include:

* camera-based social detection
* facial expression analysis
* direction of sound detection
* haptic feedback
* smartphone app deployment
* TensorFlow Lite mobile inference

---

# 19. Contribution

If other developers want to run this project:

They must:

1. Install Python 3.11
2. Create a virtual environment
3. Install dependencies
4. Run:

```
python -m orchestrator.aura_core
```

---

# 20. Project Status

Current stage:

```
Phase 1 – Audio MVP Completed
```

Working components:

```
real-time audio capture
voice detection
environment classification
decision logic
speech feedback
```

---

