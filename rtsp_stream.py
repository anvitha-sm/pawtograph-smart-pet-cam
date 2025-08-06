import subprocess
import threading
import numpy as np
import cv2
import sys
import struct
from video_preprocessing import preprocess_frame

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
SAMPLE_RATE = 44100
CHANNELS = 1

def read_video():
    video_cmd = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', RTSP_CAM,
        '-an', 
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f'{FRAME_WIDTH}x{FRAME_HEIGHT}',
        'pipe:1'
    ]
    proc = subprocess.Popen(video_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)

    while True:
        raw_frame = proc.stdout.read(FRAME_WIDTH * FRAME_HEIGHT * 3)
        if len(raw_frame) != FRAME_WIDTH * FRAME_HEIGHT * 3:
            break
        frame = np.frombuffer(raw_frame, np.uint8).reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
        frame = preprocess_frame(frame)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    proc.kill()
    cv2.destroyAllWindows()

def read_audio():
    audio_cmd = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', RTSP_AUD,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', str(SAMPLE_RATE),
        '-ac', str(CHANNELS),
        '-f', 's16le',
        'pipe:1'
    ]
    proc = subprocess.Popen(audio_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**6)

    while True:
        raw_audio = proc.stdout.read(4096)
        if not raw_audio:
            break
        # samples = np.frombuffer(raw_audio, dtype=np.int16)
        print(f"Audio chunk: {len(raw_audio)} bytes")
    proc.kill()

video_thread = threading.Thread(target=read_video)
audio_thread = threading.Thread(target=read_audio)

video_thread.start()
audio_thread.start()

video_thread.join()
audio_thread.join()
