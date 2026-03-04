from output.tts import TTS
import time


def main():
    print("===================================")
    print(" AURA TTS TEST ")
    print("===================================\n")

    tts = TTS(rate=165)

    print("Speaking first message...")
    tts.speak("Hello. This is AURA testing speech output.")

    time.sleep(3)

    print("Speaking second message quickly...")
    tts.speak("This should not overlap with the previous sentence.")

    time.sleep(5)

    print("Testing rapid calls...")
    for i in range(5):
        tts.speak(f"Test message number {i+1}")
        time.sleep(0.5)

    print("\nTTS test completed.")


if __name__ == "__main__":
    main()