import torch
import torchaudio
import numpy as np

mfcc_transform = torchaudio.transforms.MFCC(
    sample_rate=8000,  
    n_mfcc=13,
    melkwargs={"n_fft": 256, "hop_length": 128, "n_mels": 40}
)

def process_audio(raw_audio_bytes):
    audio_np = np.frombuffer(raw_audio_bytes, dtype=np.int16)
    audio_tensor = torch.from_numpy(audio_np).float()
    audio_tensor /= 32768.0
    mfcc = mfcc_transform(audio_tensor)
    return mfcc  