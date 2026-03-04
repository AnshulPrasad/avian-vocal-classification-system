import librosa
import soundfile as sf
import numpy as np

# Responsibilities:
# - Resample MP3s to 22050 Hz
# - Convert stereo to mono
# - Trim silence
# - Chunk into 5-second clips
# - Save as WAV to data/processed/

class Preprocessor:
    def __init__(self, audio, original_sr):
        self.audio = audio
        self.original_sr = original_sr

    def resample_audio(self, target_sr=22050):
        if self.original_sr == target_sr:
            resampled = self.audio.astype(np.float32)
            return resampled
        resampled = librosa.resample(self.audio, self.original_sr, self.target_sr)
        return resampled.astype(np.float32)

    def to_mono(self, audio):
        if audio.ndim == 1:
            return audio.astype(np.float32)
        monoed = librosa.to_mono(audio)
        return monoed.astype(np.float32)

    def trim_silence(self, audio):
        audio_trim, _ = librosa.effects.trim(audio)
        return audio_trim.astype(np.float32)

    def chunk_audio(self, audio, sr=22050, duration=5):
        clip = audio[:sr * duration]  # take first 5 seconds
        clip = librosa.util.fix_length(clip, size=sr * duration)  # pad if short
        return clip.astype(np.float32)

    def save_audio(self, audio, output_path, sr=22050):
        sf.write(output_path, audio, samplerate=sr)
