import tensorflow as tf
import tensorflow_hub as hub
import numpy as np


class AmbientClassifier:
    def __init__(self):
        """
        Loads pretrained YAMNet model from TensorFlow Hub.
        YAMNet expects 16kHz mono waveform input.
        """
        self.model = hub.load("https://tfhub.dev/google/yamnet/1")
        self.class_names = self._load_class_names()

    def _load_class_names(self):
        """
        Load YAMNet class names.
        """
        class_map_path = self.model.class_map_path().numpy()
        class_names = []

        with open(class_map_path) as f:
            for line in f.readlines()[1:]:
                class_names.append(line.strip().split(",")[2])

        return class_names

    def classify(self, audio_waveform):
        """
        Classifies environment using top-3 predictions for stability.
        """

        waveform = tf.convert_to_tensor(audio_waveform, dtype=tf.float32)

        scores, embeddings, spectrogram = self.model(waveform)

        mean_scores = tf.reduce_mean(scores, axis=0)

        scores_np = mean_scores.numpy()

        # Get top 3 predictions
        top_indices = np.argsort(scores_np)[-3:][::-1]

        top_labels = []
        top_confidences = []

        for idx in top_indices:
            label = self.class_names[idx]
            conf = scores_np[idx]

            top_labels.append(label)
            top_confidences.append(conf)

            # print(f"[YAMNET RAW] {label} | confidence={conf:.2f}")

        # Map all top labels
        mapped = [self._map_to_environment(label) for label in top_labels]

        # Majority vote
          # Priority based decision (speech should dominate)

        if "conversational" in mapped:
           final_label = "conversational"

        elif "traffic" in mapped:
           final_label = "traffic"

        elif "music" in mapped:
           final_label = "music"

        elif "noisy" in mapped:
           final_label = "noisy"

        else:
           final_label = "quiet"

        confidence = float(np.max(top_confidences))

        return final_label, confidence

    def _map_to_environment(self, yamnet_label):
        """
        Maps YAMNet classes into meaningful AURA environments.
        """

        label = yamnet_label.lower()

        # conversational
        if "speech" in label or "conversation" in label or "narration" in label:
            return "conversational"

        # music
        if "music" in label or "musical" in label:
            return "music"

        # traffic
        if (
            "vehicle" in label
            or "car" in label
            or "truck" in label
            or "engine" in label
            or "traffic" in label
            or "horn" in label
        ):
            return "traffic"

        # noisy environment
        if (
            "noise" in label
            or "buzz" in label
            or "hum" in label
            or "fan" in label
            or "mechanical" in label
            or "mechanism" in label
            or "insect" in label
        ):
            return "noisy"

        # default
        return "quiet"
