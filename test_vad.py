from audio_capture.mic_stream import MicStream
from vad.vad_engine import VADEngine


def main():
    print("===================================")
    print(" AURA VAD TEST (Real-Time Mode) ")
    print(" Speak clearly into the microphone.")
    print(" Press Ctrl+C to stop.")
    print("===================================\n")

    mic = MicStream()
    vad = VADEngine(
    aggressiveness=2,          # slightly less strict
    speech_ratio_threshold=0.55,  # slightly lower threshold
    energy_threshold=0.015     # allow softer speech
)

    try:
        for audio_frame in mic.audio_generator():
            speech = vad.is_speech(audio_frame)

            if speech:
                print(">>> SPEECH DETECTED <<<")
            else:
                print("Silence")

    except KeyboardInterrupt:
        print("\nVAD test stopped manually.")


if __name__ == "__main__":
    main()