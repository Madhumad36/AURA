import time
from collections import deque
from utils.logger import AuraLogger
from audio_capture.mic_stream import MicStream
from vad.vad_engine import VADEngine
from audio_classification.ambient_classifier import AmbientClassifier
from decision_engine.rule_engine import RuleEngine
from decision_engine.context_engine import ContextEngine
from output.tts import TTS


def main(duration=30):  

    print("===================================")
    print(" AURA - Real Time Assistive System ")
    print(" Running for limited duration...")
    print("===================================\n")

    # Initialize modules
    mic = MicStream()
    vad = VADEngine(
        aggressiveness=3,
        speech_ratio_threshold=0.8,
        energy_threshold=0.04
    )

    classifier = AmbientClassifier()

    rule_engine = RuleEngine(
        cooldown_seconds=20,
        confidence_threshold=0.5
    )

    context_engine = ContextEngine(window_size=10)
    tts = TTS(rate=165)
    logger = AuraLogger()

    label_buffer = deque(maxlen=5)

    print("AURA is listening to the environment...", flush=True)

    last_message = None
    last_context = None
    last_stable_label = None
    label_hold_count = 0

    HOLD_THRESHOLD = 3

    # TIMER START
    start_time = time.time()

    try:
        for audio_frame in mic.audio_generator():

            #  STOP AFTER DURATION
            if time.time() - start_time > duration:
                print("\n Audio time limit reached")
                break

            # 1️⃣ VAD
            vad_active = vad.is_speech(audio_frame)

            # 2️⃣ Classification
            label, confidence = classifier.classify(audio_frame)
            if label is None:
                continue

            # 🔹 Smoothing buffer
            label_buffer.append(label)
            if len(label_buffer) < 5:
                continue

            # 🔹 Majority vote
            stable_label = max(set(label_buffer), key=label_buffer.count)

            # 🔹 Hold logic
            if last_stable_label is None:
                last_stable_label = stable_label

            if stable_label == last_stable_label:
                label_hold_count = 0
            else:
                label_hold_count += 1

            if label_hold_count < HOLD_THRESHOLD:
                stable_label = last_stable_label
            else:
                last_stable_label = stable_label
                label_hold_count = 0

            print(f"[DEBUG] label={stable_label}, confidence={confidence:.2f}, vad={vad_active}")

            #  Logging
            logger.log(stable_label, confidence, vad_active)

            #  Override VAD for non-speech
            if stable_label in ["noisy", "traffic", "music"]:
                vad_active = False

            #  Context Engine
            context_engine.update(stable_label)
            context = context_engine.get_context()

            #  Rule Engine
            message = rule_engine.evaluate(
                environment_label=stable_label,
                confidence=confidence,
                vad_active=vad_active
            )

            #  Speak 
            if context and context != last_context:
                print(f"AURA says: You are in a {context}", flush=True)
                tts.speak(f"You are in a {context}")
                last_context = context

            elif message:
                if message != last_message:
                    print(f"AURA says: {message}", flush=True)
                    tts.speak(message)
                    last_message = message

    except KeyboardInterrupt:
        print("\nAURA stopped manually.")



if __name__ == "__main__":
    main()