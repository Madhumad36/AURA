import pyttsx3


class TTS:
    def __init__(self, rate=165):
        self.rate = rate

    def speak(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', self.rate)
        engine.say(text)
        engine.runAndWait()
        engine.stop()