import librosa
import numpy as np
from pydub import AudioSegment
from io import BytesIO
import random
import os
from imports.baseclass import BaseClass
import base64

class AudioDataSet(BaseClass):
    def __init__(self, file_path):
        # Load the audio file
        self.file_path = file_path
        self.audio, self.sr = librosa.load(file_path, sr=None)
    
    @property
    def contents(self) -> str:
        # returns file name for playing the audio file in flask api
        return os.path.basename(self.file_path)

    # function to convert PIP images to base64
    def audio_to_base64(self, audio_segment) -> str:
        """Convert an AudioSegment object to a base64 string."""
        # Save to a byte buffer
        byte_io = BytesIO()
        audio_segment.export(byte_io, format='wav')
        byte_io.seek(0)

        # Encode the byte data to base64
        return base64.b64encode(byte_io.read()).decode('utf-8')

    def numpy_to_audiosegment(self, np_audio, sr) -> AudioSegment:
        """Convert a numpy array to a pydub AudioSegment."""
        # Ensure the numpy array is in a proper format for AudioSegment (PCM format, mono)
        return AudioSegment(
            np_audio.tobytes(), 
            frame_rate=sr,
            sample_width=np_audio.dtype.itemsize,
            channels=1
        )

    # Preprocessing Methods
    def preprocess_all(self):
        # 1. Normalize the audio to be in a consistent volume range
        normalized_audio = librosa.util.normalize(self.audio)
        
        # 2. Trim silence from the beginning and end
        trimmed_audio, _ = librosa.effects.trim(normalized_audio)
        
        # 3. Downsample to 16kHz
        downsampled_audio = librosa.resample(trimmed_audio, orig_sr=self.sr, target_sr=16000)

        # Convert numpy arrays to AudioSegment objects
        normalized_audio_segment = self.numpy_to_audiosegment(normalized_audio, self.sr)
        trimmed_audio_segment = self.numpy_to_audiosegment(trimmed_audio, self.sr)
        downsampled_audio_segment = self.numpy_to_audiosegment(downsampled_audio, 16000)

        # Encode each as base64
        preprocessed_audio = {
            'normalized_audio': self.audio_to_base64(normalized_audio_segment),
            'trimmed_audio': self.audio_to_base64(trimmed_audio_segment),
            'downsampled_audio': self.audio_to_base64(downsampled_audio_segment)
        }

        return preprocessed_audio

    # Augmentation Methods
    def augment_all(self):
        # 1. Add white noise
        noise = np.random.normal(0, 0.005, self.audio.shape)
        noisy_audio = self._to_audio_segment(self.audio + noise)
        
        # 2. Pitch shift by 2 semitones up
        pitch_shifted_audio = self._to_audio_segment(librosa.effects.pitch_shift(self.audio, sr=self.sr, n_steps=2))
        
        # 3. Time stretch (speed up by 10%)
        stretched_audio = self._to_audio_segment(librosa.effects.time_stretch(self.audio, rate=1.1))

        # return {
        #     'noisy': self._to_audio_segment(noisy_audio),
        #     'pitch_shifted': self._to_audio_segment(pitch_shifted_audio),
        #     'stretched': self._to_audio_segment(stretched_audio)
        # }
        augmented_audio = {
            key: self.audio_to_base64(audio) for key, audio in {
                'noisy_audio': noisy_audio,
                'pitch_shifted_audio': pitch_shifted_audio,
                'stretched_audio': stretched_audio
            }.items()
        }
        return augmented_audio

    # Helper method to convert numpy audio data to an AudioSegment
    def _to_audio_segment(self, audio_data, target_sr=None):
        target_sr = target_sr if target_sr else self.sr
        audio_data = (audio_data * 32767).astype(np.int16)  # Convert to 16-bit PCM format
        audio_segment = AudioSegment(
            data=audio_data.tobytes(),
            sample_width=2,  # 16-bit audio
            frame_rate=target_sr,
            channels=1
        )
        return audio_segment

    # Helper method to convert AudioSegment to a BytesIO object for Flask
    def audio_to_bytesio(self, audio_segment):
        audio_io = BytesIO()
        audio_segment.export(audio_io, format="mp3")
        audio_io.seek(0)
        return audio_io
