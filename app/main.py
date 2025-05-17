from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import uuid

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")
)

FRENCH_VOICE_ID = "MF3mGyEYCl7XYWbV9V6O"
MODEL_ID = "eleven_multilingual_v2"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel) : 
    text : str

@app.post("/generate_speech/")
async def generate_speech(request: TextRequest):
    text = request.text
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("/tmp", filename)  

    audio_stream = client.text_to_speech.convert_as_stream(
        text=text,
        voice_id=FRENCH_VOICE_ID,
        model_id=MODEL_ID
    )

    
    with open(filepath, "wb") as f:
        for chunk in audio_stream:
            if isinstance(chunk, bytes):
                f.write(chunk)

    return FileResponse(filepath, media_type="audio/mpeg", filename=filename)
