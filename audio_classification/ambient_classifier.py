import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from collections import deque
from collections import Counter


class AmbientClassifier:
    def __init__(self,
                 confidence_threshold=0.4,
                 smoothing_window=3):

        self.model = hub.load("https://tfhub.dev/google/yamnet/1")
        self.class_names = self._load_class_names()

        self.confidence_threshold = confidence_threshold
        self.smoothing_window = smoothing_window

        # Store last N predictions
        self.prediction_buffer = deque(maxlen=smoothing_window)

    def _load_class_names(self):
        class_map_path = self.model.class_map_path().numpy()
        class_names = []

        with open(class_map_path) as f:
            for line in f.readlines()[1:]:
                class_names.append(line.strip().split(",")[2])

        return class_names

    def classify(self, audio_waveform):

        waveform = tf.convert_to_tensor(audio_waveform, dtype=tf.float32)

        scores, embeddings, spectrogram = self.model(waveform)

        mean_scores = tf.reduce_mean(scores, axis=0)

        top_index = tf.argmax(mean_scores).numpy()
        confidence = float(tf.reduce_max(mean_scores).numpy())

        raw_label = self.class_names[top_index]
        mapped_label = self._map_to_environment(raw_label)

        # Ignore weak predictions
        if confidence < self.confidence_threshold:
            return None, 0.0

        # Add to smoothing buffer
        self.prediction_buffer.append(mapped_label)

        # Only smooth when buffer full
        if len(self.prediction_buffer) < self.smoothing_window:
            return None, 0.0

        # Majority vote
        label_counts = Counter(self.prediction_buffer)
        smoothed_label, count = label_counts.most_common(1)[0]

        # Require at least 2 out of 3 agreement
        if count >= 2:
            return smoothed_label, confidence

        return None, 0.0

    def _map_to_environment(self, yamnet_label):
        label = yamnet_label.lower()

        if "speech" in label or "conversation" in label:
            return "conversational"

        elif "crowd" in label or "applause" in label:
            return "crowded"

        elif (
            "traffic" in label or
            "engine" in label or
            "noise" in label or
            "clap" in label or
            "bang" in label or
            "knock" in label or
            "impact" in label or
            "door" in label or
            "footstep" in label or
            "typing" in label
        ):
            return "noisy"

        else:
            return "quiet"


# ===========================
# 🔍 TEST BLOCK
# ===========================

if __name__ == "__main__":

    from audio_capture.mic_stream import MicStream

    print("===================================")
    print(" AURA Ambient Classifier Test ")
    print(" Using Temporal Smoothing (3-frame)")
    print("===================================\n")

    mic = MicStream()
    classifier = AmbientClassifier()

    try:
        for audio_frame in mic.audio_generator():

            label, confidence = classifier.classify(audio_frame)

            if label is None:
                print("No stable prediction.")
                continue

            print(f"Detected Environment: {label}")
            print(f"Confidence: {confidence:.2f}")
            print("-----------------------------------")

    except KeyboardInterrupt:
        print("\nTest stopped manually.")