from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
import edge_tts
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MASCULINE_VOICE = "fr-FR-HenriNeural"

@app.post("/generate_speech/")
async def generate_speech(text: str):
    
    filename = f"{uuid.uuid4().hex}.mp3"

    communicate = edge_tts.Communicate(text, voice=MASCULINE_VOICE)
    await communicate.save(filename)

    return FileResponse(filename, media_type="audio/mp3", filename="speech.mp3")
