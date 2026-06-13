from collections import deque


class ContextEngine:
    def __init__(self, window_size=10):
        self.window = deque(maxlen=window_size)

    def update(self, label):
        self.window.append(label)

    def get_context(self):
        if len(self.window) < 5:
            return None  # not enough data

        counts = {l: self.window.count(l) for l in set(self.window)}

        # Dominant label
        dominant = max(counts, key=counts.get)

        # Context rules
        if dominant == "conversational":
            return "active conversation"

        elif dominant in ["noisy", "traffic"]:
            return "busy environment"

        elif dominant == "music":
            return "music playing nearby"

        elif dominant == "quiet":
            return "calm environment"

        return None