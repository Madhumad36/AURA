import time
from decision_engine.rule_engine import RuleEngine


def main():
    rule_engine = RuleEngine(cooldown_seconds=5)

    test_sequence = [
        ("Quiet", 0.9, False),           # Speak immediately
        ("Quiet", 0.9, False),           # No speech (cooldown)
        ("Conversational", 0.9, True),   # Delay (VAD active)
        ("Conversational", 0.9, True),   # Still delay
        ("Conversational", 0.9, False),  # Speech stopped → now speak
        ("Conversational", 0.9, False),  # Cooldown block
    ]

    for label, confidence, vad in test_sequence:
        message = rule_engine.evaluate(label, confidence, vad)

        if message:
            print("AURA would say:", message)
        else:
            print("No speech.")

        time.sleep(2)


if __name__ == "__main__":
    main()