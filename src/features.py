import librosa
import numpy as np
from preprocess import Preprocessor
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import shutil
from pathlib import Path

# Responsibilities:
# - Generate mel spectrograms from processed WAVs
# - Apply augmentation (noise, pitch shift, time stretch)
# - Save spectrograms as PNGs to data/spectrograms/
# - Split into train/val/test

class FeatureExtractor ():

    def __init__(self, audio, original_sr):
        self.audio = audio
        self.original_sr = original_sr

    def generate_melspectrogram(self, audio, n_mels=128, hop_length=512):
        mel = librosa.feature.melspectrogram(y=audio, n_mels=n_mels, hop_length=hop_length)
        mel_db = librosa.power_to_db(mel, ref=np.max) # convert to decibels
        return mel_db

    def augment_audio(self, audio, sr):
        stretched = librosa.effects.time_stretch(audio, rate= np.random.uniform(0.8,1.2)) # time stretched
        pitched = librosa.effects.pitch_shift(audio, sr=sr, n_steps=np.random.randint(-2,2)) # pitch shift
        noise = np.random.normal(0, 0.005, len(audio)) # add background noise
        noisy = self.audio + noise
        return stretched, pitched, noisy


    def save_spectrogram(self, spectrogram, path, hop_length=512, x_axis="time", y_axis="mel"):
        np.save(path, spectrogram)
        plt.figure(figsize=(8,3))
        librosa.display.specshow(spectrogram, hop_length=hop_length, x_axis=x_axis, y_axis=y_axis).plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()

    def split_dataset(self, species_dir, output_dir, splits=(0.7, 0.15, 0.15)):
        files = list(Path(species_dir).rglob("*.png"))  # mel spectrogram images
        train, temp = train_test_split(files, test_size=1 - splits[0], random_state=42)
        val, test = train_test_split(temp, test_size=0.5, random_state=42)

        for split_name, split_files in [("train", train), ("val", val), ("test", test)]:
            for f in split_files:
                dest = Path(output_dir) / split_name / f.parent.name
                dest.mkdir(parents=True, exist_ok=True)
                shutil.copy(f, dest)