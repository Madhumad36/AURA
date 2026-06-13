import librosa
import numpy as np

class AudioPreprocessor:
    def __init__(self, sample_rate=16000, n_mels=64):
        """
        sample_rate: sampling frequency of input audio
        n_mels: number of Mel frequency bands
        """
        self.sample_rate = sample_rate
        self.n_mels = n_mels

    def extract_log_mel(self, audio_signal):
        """
        Converts raw audio waveform into a log-Mel spectrogram.

        audio_signal: 1D numpy array (length = sample_rate * duration)
        """
        # Generate Mel spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=audio_signal,
            sr=self.sample_rate,
            n_mels=self.n_mels,
            hop_length=512,
            n_fft=1024
        )

        # Convert to log scale
        log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

        return log_mel_spec


