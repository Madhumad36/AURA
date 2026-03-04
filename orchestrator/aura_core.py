import time

from audio_capture.mic_stream import MicStream
from vad.vad_engine import VADEngine
from audio_classification.ambient_classifier import AmbientClassifier
from decision_engine.rule_engine import RuleEngine
from output.tts import TTS


def main():

    print("===================================")
    print(" AURA - Real Time Assistive System ")
    print(" Press Ctrl+C to stop.")
    print("===================================\n")

    # Initialize modules
    mic = MicStream()
    vad = VADEngine(
        aggressiveness=2,
        speech_ratio_threshold=0.55,
        energy_threshold=0.015
    )

    classifier = AmbientClassifier(
        confidence_threshold=0.4,
        smoothing_window=2
    )

    rule_engine = RuleEngine(
        cooldown_seconds=20,
        confidence_threshold=0.5
    )

    tts = TTS(rate=165)

    try:
        for audio_frame in mic.audio_generator():

            # 1️⃣ Check speech activity
            vad_active = vad.is_speech(audio_frame)

            # 2️⃣ Classify environment
            label, confidence = classifier.classify(audio_frame)

            if label is None:
                continue

            # 3️⃣ Decide whether to speak
            message = rule_engine.evaluate(
                environment_label=label,
                confidence=confidence,
                vad_active=vad_active
            )

            # 4️⃣ Speak if needed
            if message:
                print(f"AURA says: {message}")
                tts.speak(message)

    except KeyboardInterrupt:
        print("\nAURA stopped manually.")


if __name__ == "__main__":
    main()