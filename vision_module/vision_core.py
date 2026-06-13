import warnings
warnings.filterwarnings("ignore")

import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import cv2
import time
import math
import pandas as pd
from ultralytics import YOLO
from gtts import gTTS

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


# sPEECH

import os
import platform

def speak(text):
    tts = gTTS(text)
    filename = "output.mp3"
    tts.save(filename)

    # Play audio depending on OS
    if platform.system() == "Windows":
        os.system(f'start {filename}')
    elif platform.system() == "Darwin":
        os.system(f'afplay {filename}')
    else:
        os.system(f'mpg123 {filename}')

    return filename

# LOAD MODELS

print("Loading models...")

model = YOLO("yolov8x.pt")

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


# BLIP CAPTION

def generate_caption(frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    inputs = processor(image, return_tensors="pt")
    out = blip_model.generate(**inputs, max_new_tokens=25)
    return processor.decode(out[0], skip_special_tokens=True)


#  PROXIMITY

def get_center(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2)//2, (y1 + y2)//2)

def is_close(boxes, threshold=150):
    if len(boxes) < 2:
        return False
    centers = [get_center(b) for b in boxes]
    for i in range(len(centers)):
        for j in range(i+1, len(centers)):
            if math.dist(centers[i], centers[j]) < threshold:
                return True
    return False


#  CONTEXT

def infer_context(signals):
    if signals["people"] >= 2 and signals["people_close"]:
        return f"People interacting in a {signals['environment']} setting."

    if signals["animals"] >= 2 and signals["animals_close"]:
        return "Animals interacting nearby."

    if signals["motion"] == "approaching":
        return "A subject is approaching."

    if signals["density"] == "high":
        return f"Crowded {signals['environment']} environment."

    if signals["density"] == "medium":
        return f"Moderately active {signals['environment']} environment."

    if signals["people"] == 1:
        return f"Single person in a {signals['environment']} environment."

    return f"Low activity {signals['environment']} scene."


# ENVIRONMENT

def detect_environment(people, vehicles):
    if vehicles > 0:
        return "urban"
    elif people > 0:
        return "indoor/social"
    else:
        return "open/nature"


# MAIN FUNCTION 

def run_vision(video_path):

    if not video_path:
        raise Exception("No video provided")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Cannot open video")

    prev_area = None
    frame_count = 0

    last_message = None
    output_count = 0
    max_outputs = 2

    start_time = time.time()
    max_runtime = 60

    stable_counter = 0

    caption_generated = False
    caption_text = ""

    logs = []

    print("\n===== VISION SYSTEM STARTED =====\n")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if time.time() - start_time > max_runtime:
            print("Time limit reached")
            break

        frame_count += 1

        if frame_count % 12 != 0:
            continue

        results = model(frame)[0]

        people_boxes, animal_boxes, vehicle_boxes = [], [], []
        max_area = 0

        total_conf = 0
        count_conf = 0

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if conf < 0.7:
                continue

            total_conf += conf
            count_conf += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            b = (x1, y1, x2, y2)

            if cls == 0:
                people_boxes.append(b)
                area = (x2-x1)*(y2-y1)
                max_area = max(max_area, area)

            elif cls in [15,16,17,18,19,20,21,22,23]:
                animal_boxes.append(b)

            elif cls in [2,3,5,7]:
                vehicle_boxes.append(b)

        people = len(people_boxes)
        animals = len(animal_boxes)
        vehicles = len(vehicle_boxes)

        avg_conf = total_conf / count_conf if count_conf > 0 else 0

        total = people + animals + vehicles
        density = "low" if total <= 2 else "medium" if total <= 5 else "high"

        people_close = is_close(people_boxes)
        animals_close = is_close(animal_boxes)

        motion = "none"
        if prev_area and prev_area > 0 and max_area > 0:
            if (max_area - prev_area)/prev_area > 0.3:
                motion = "approaching"

        prev_area = max_area

        environment = detect_environment(people, vehicles)

        signals = {
            "people": people,
            "animals": animals,
            "vehicles": vehicles,
            "density": density,
            "people_close": people_close,
            "animals_close": animals_close,
            "motion": motion,
            "environment": environment,
            "confidence": round(avg_conf, 2)
        }

        logs.append(signals)

        if not caption_generated:
            caption_text = generate_caption(frame)
            caption_generated = True

        message = f"{caption_text}. {infer_context(signals)}"

        if message != last_message and output_count < max_outputs:
            print(message)
            speak(message)
            last_message = message
            output_count += 1

        if message == last_message:
            stable_counter += 1
        else:
            stable_counter = 0

        if stable_counter >= 3:
            print(" Scene stabilized")
            break

    cap.release()

    df = pd.DataFrame(logs)

    try:
        df.to_csv("vision_analysis.csv", mode='a',
                  header=not os.path.exists("vision_analysis.csv"),
                  index=False)
    except PermissionError:
        df.to_csv("vision_analysis_backup.csv", index=False)

    summary = f"Scene interpreted. {caption_text}"
    print(summary)

    return summary, df
