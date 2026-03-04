import webrtcvad
import numpy as np


class VADEngine:
    def __init__(self, sample_rate=16000, frame_duration_ms=30,
                 aggressiveness=3,
                 speech_ratio_threshold=0.6,
                 energy_threshold=0.02):
        """
        sample_rate: must be 16000
        frame_duration_ms: 10, 20, or 30 ms (30 is more stable)
        aggressiveness: 0–3 (3 = strictest)
        speech_ratio_threshold: percentage of frames needed to detect speech
        energy_threshold: minimum RMS energy to consider valid speech
        """

        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.vad = webrtcvad.Vad(aggressiveness)

        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.speech_ratio_threshold = speech_ratio_threshold
        self.energy_threshold = energy_threshold

    def _float_to_int16(self, audio_signal):
        audio_signal = np.clip(audio_signal, -1.0, 1.0)
        return (audio_signal * 32767).astype(np.int16)

    def _rms_energy(self, audio_signal):
        return np.sqrt(np.mean(audio_signal ** 2))

    def is_speech(self, audio_signal):
        """
        Determines if speech is present in 1-second audio chunk.
        Returns True or False.
        """

        # 1️⃣ Energy filter first (ignore very low-level noise)
        energy = self._rms_energy(audio_signal)

        if energy < self.energy_threshold:
            return False

        int16_audio = self._float_to_int16(audio_signal)

        speech_frames = 0
        total_frames = 0

        for start in range(0, len(int16_audio) - self.frame_size, self.frame_size):
            frame = int16_audio[start:start + self.frame_size]
            total_frames += 1

            if self.vad.is_speech(frame.tobytes(), self.sample_rate):
                speech_frames += 1

        ratio = speech_frames / total_frames if total_frames > 0 else 0

        if ratio > self.speech_ratio_threshold:
            return True

        return False