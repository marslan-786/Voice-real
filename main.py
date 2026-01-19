import os
import uvicorn
from fastapi import FastAPI, Form, Response
# 👇 This trick fixes the "WeightsUnpickler" error
import torch
torch.serialization.add_safe_globals = lambda *args, **kwargs: None 
from TTS.api import TTS

print("⏳ Loading XTTS v2 Model (This will utilize your 32GB RAM)...")
device = "cpu"

# Load Model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.get("/")
def home():
    return {"status": "XTTS Cloning Server Ready 🧬"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    print(f"🎙️ Cloning Request: {text[:30]}...")
    output_path = "output.wav"
    
    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Error: 'my_voice.wav' not found!", status_code=500)

    try:
        tts.tts_to_file(
            text=text,
            speaker_wav=SPEAKER_WAV,
            language="hi", # Hindi engine handles Urdu perfectly
            file_path=output_path
        )
        
        with open(output_path, "rb") as f:
            audio_data = f.read()
            
        return Response(content=audio_data, media_type="audio/wav")
        
    except Exception as e:
        print(f"❌ XTTS Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))