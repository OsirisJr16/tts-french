from fastapi import FastAPI
from gtts import gTTS
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/generate_speech/")
async def generate_speech(text: str):
   
    tts = gTTS(text, lang='fr')
    output_file = "output.mp3"

    tts.save(output_file)
    

    return FileResponse(output_file, media_type="audio/mp3", filename="output.mp3")
