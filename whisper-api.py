from fastapi import FastAPI, File, UploadFile
from faster_whisper import WhisperModel
import shutil
import os

app = FastAPI()

model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

@app.get("/")
async def root():
    return {"message": "Welcome to the transcription API"}

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    with open("temp_audio.mp3", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Perform transcription
    segments, info = model.transcribe("temp_audio.mp3", beam_size=5)
    # Remove the temporary file
    os.remove("temp_audio.mp3")
    text = ' '.join(segment.text for segment in segments)
    return text