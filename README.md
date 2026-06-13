# AURA: Real-Time Audio Scene and Social Contextualizer

## Overview

AURA is a multi-layer environment understanding system designed to interpret surroundings using both audio and visual perception. The project combines real-time audio scene analysis with vision-based scene understanding to generate meaningful contextual descriptions rather than simple detections.

The system consists of two independent perception layers:

1. Audio Layer – Real-time environmental sound analysis
2. Vision Layer – Video-based scene understanding

Both layers are integrated through a unified Streamlit interface that presents textual outputs, speech feedback, structured logs, and graphical insights.

---

## Project Objectives

- Analyze environmental sounds in real time.
- Understand visual scenes from video input.
- Generate context-aware interpretations instead of raw detections.
- Provide outputs in text, speech, and graphical formats.
- Demonstrate a multi-modal approach to environment understanding.

---

# System Architecture

Input Layer
│
├── Audio Module (Real-Time)
│ ├── Audio Capture
│ ├── Voice Activity Detection (VAD)
│ ├── Environmental Classification
│ ├── Context Generation
│ └── Rule-Based Interpretation
│
├── Vision Module (Video Input)
│ ├── Frame Extraction
│ ├── Object Detection (YOLOv8)
│ ├── Image Captioning (BLIP)
│ ├── Context Generation
│ └── Scene Interpretation
│
└── Unified Interface (Streamlit)
│
├── Text Output
├── Speech Output
├── Data Tables
└── Graphical Insights

---

# Audio Module

## Description

The audio module continuously captures sound from the system microphone and performs real-time environmental analysis.

The module identifies environmental conditions such as:

- Conversational environments
- Noisy environments
- Traffic environments
- Music environments
- Quiet environments

To improve reliability, prediction smoothing and temporal context analysis are applied before generating outputs.

---

## Audio Processing Pipeline

Microphone Input
↓
Voice Activity Detection (VAD)
↓
Audio Classification
↓
Prediction Stabilization
↓
Context Generation
↓
Rule-Based Interpretation
↓
Speech & Text Output

---

## Key Features

- Real-time audio processing
- Voice Activity Detection (VAD)
- Environmental sound classification
- Context-aware interpretation
- Prediction smoothing using buffer windows
- Speech feedback using Text-to-Speech
- CSV-based logging for analysis

---

## Audio Outputs

The audio module generates:

- Real-time contextual messages
- Speech output
- Confidence values
- Environmental labels
- Activity logs

### Visual Analytics

- Confidence Trend
- Environment Distribution
- Voice Activity Detection (VAD) Analysis
- Summary Metrics

---

# Vision Module

## Description

The vision module analyzes uploaded video files and generates scene-level understanding using deep learning models.

Instead of merely detecting objects, the module combines object detection and semantic captioning to infer contextual information about the environment.

---

## Technologies Used

- YOLOv8 for object detection
- BLIP for image captioning
- OpenCV for video processing
- Pandas for data management

---

## Vision Processing Pipeline

Video Input
↓
Frame Extraction
↓
Object Detection (YOLOv8)
↓
Caption Generation (BLIP)
↓
Feature Extraction
↓
Context Inference
↓
Scene Interpretation
↓
Text & Speech Output

---

## Contextual Features Extracted

The vision module evaluates:

- Object presence
- Human density
- Animal presence
- Vehicle presence
- Object proximity
- Scene activity
- Motion patterns
- Environmental characteristics

---

## Vision Outputs

The vision module generates:

- Scene Interpretation
- Speech Narration
- Detection Data Table
- System Interpretation
- System Confidence Indicator
- Activity Analysis Graphs

---

# User Interface

The system interface is implemented using Streamlit and provides a unified platform for executing both modules.

---

## Audio Mode

Features:

- Duration selection
- Real-time recording
- Log visualization
- Analytical graphs
- Summary metrics

---

## Vision Mode

Features:

- Video upload
- Automated processing
- Scene interpretation
- Speech output
- Data visualization
- Behavioral analysis

---

# Experimental Setup

## Hardware

- Intel i5/i7 Processor
- 8 GB RAM or higher
- Microphone
- Laptop/Desktop Computer

---

## Software

- Windows Operating System
- Python 3.x
- Visual Studio Code
- Streamlit

---

## Libraries

- Ultralytics YOLO
- Transformers (BLIP)
- OpenCV
- NumPy
- Pandas
- PyAudio
- Voice Activity Detection (VAD)
- gTTS

---

# Applications

- Assistive technology
- Environmental monitoring
- Smart perception systems
- Human-environment interaction
- Context-aware computing
- Educational and research demonstrations

---

# Future Scope

- Real-time camera integration
- Multi-modal fusion between audio and vision
- Edge-device deployment
- Improved context reasoning
- Enhanced visualization and analytics
- Expanded environmental understanding capabilities

---

# Conclusion

AURA demonstrates a practical approach to multi-layer environment understanding by combining audio scene analysis and visual scene interpretation. Through contextual reasoning and multimodal perception, the system provides meaningful descriptions of real-world environments using text, speech, and graphical outputs. The project establishes a scalable foundation for future intelligent perception systems and context-aware applications.
