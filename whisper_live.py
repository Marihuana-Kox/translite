import queue
import sys
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

# Загружаем модель
model = WhisperModel("base", device="cpu", compute_type="int8")

samplerate = 16000
blocksize = 4000
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, blocksize=blocksize):
    print("🎤 Говори...")
    buffer = np.zeros((0, 1), dtype=np.float32)
    while True:
        data = q.get()
        buffer = np.concatenate((buffer, data), axis=0)

        if len(buffer) >= samplerate * 5:  # каждые ~5 секунд
            audio_chunk = buffer[:samplerate * 5]
            buffer = buffer[samplerate * 5:]

            segment, _ = model.transcribe(audio_chunk.flatten(), language="de", beam_size=1)
            full_text = "".join([s.text for s in segment])
            print("🗣️", full_text.strip())
