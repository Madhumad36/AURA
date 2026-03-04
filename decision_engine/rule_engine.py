import time


class RuleEngine:
    def __init__(self,
                 cooldown_seconds=20,
                 confidence_threshold=0.5):

        self.cooldown_seconds = cooldown_seconds
        self.confidence_threshold = confidence_threshold

        self.last_environment = None
        self.last_spoken_time = 0

        self.pending_environment = None
        self.pending_message = None

    def evaluate(self, environment_label, confidence, vad_active):
        current_time = time.time()

        if confidence < self.confidence_threshold:
            return None

        # 1️⃣ Environment changed
        if environment_label != self.last_environment:

            message = self._generate_message(environment_label)

            # Update environment immediately
            self.last_environment = environment_label

            if vad_active:
                # Store pending but DO NOT speak yet
                self.pending_environment = environment_label
                self.pending_message = message
                return None

            # Speak immediately
            self.last_spoken_time = current_time
            return message

        # 2️⃣ If pending exists and speech stopped
        if self.pending_message and not vad_active:

            message = self.pending_message

            self.pending_environment = None
            self.pending_message = None

            self.last_spoken_time = current_time
            return message

        # 3️⃣ Cooldown reminder
        if (not vad_active and
                current_time - self.last_spoken_time >= self.cooldown_seconds):

            self.last_spoken_time = current_time
            return self._generate_message(environment_label)

        return None

    def _generate_message(self, environment_label):
        messages = {
            "Quiet": "The environment is quiet.",
            "Conversational": "People are having conversations nearby.",
            "Crowded": "The environment is crowded.",
            "Music": "Music is playing nearby.",
            "Noise": "There is noticeable background noise."
        }

        return messages.get(
            environment_label,
            f"The environment is {environment_label.lower()}."
        )