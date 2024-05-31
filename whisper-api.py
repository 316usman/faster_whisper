from fastapi import FastAPI, File, UploadFile
from faster_whisper import WhisperModel
import shutil
import os
import time

app = FastAPI()

model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

async def transcribe_audio_async(file_path):
    segments, info = model.transcribe(file_path, beam_size=5)
    text = ' '.join(segment.text for segment in segments)
    return text

@app.get("/")
async def root():
    return {"message": "Welcome to the transcription API"}

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    file_path = "temp_audio.mp3"
    # Save the uploaded file to a temporary location
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Perform transcription
    text = await transcribe_audio_async(file_path)
    os.remove(file_path)
    return text