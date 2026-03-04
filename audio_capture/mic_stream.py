import sounddevice as sd
import numpy as np
from queue import Queue

class MicStream:
    def __init__(self, sample_rate=16000, chunk_duration=1.0):
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_size = int(sample_rate * chunk_duration)

        self.audio_queue = Queue()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print("Audio status:", status)

        # Flatten (frames, 1) → (frames,)
        self.audio_queue.put(np.squeeze(indata.copy()))

    def audio_generator(self):
        """
        Yields audio chunks continuously using a single open stream.
        """
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=self.chunk_size,
            callback=self._audio_callback
        ):
            while True:
                audio_chunk = self.audio_queue.get()
                yield audio_chunk
if __name__ == "__main__":
    mic = MicStream()
    for audio in mic.audio_generator():
        print("Captured audio frame:", audio.shape)
        

