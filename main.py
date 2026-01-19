import os
import uvicorn
from fastapi import FastAPI, Form, Response
from TTS.api import TTS
import torch

# 🚀 Load XTTS v2 (The Beast)
print("⏳ Loading XTTS v2 Model (This will utilize your 32GB RAM)...")
device = "cpu"

# یہ پہلی بار ماڈل ڈاؤن لوڈ کرے گا (تقریباً 2-3 GB)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

app = FastAPI()

# 🎤 آپ کی آواز کی فائل کا نام
SPEAKER_WAV = "male_voice.wav"

@app.get("/")
def home():
    return {"status": "XTTS Cloning Server Ready 🧬"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    print(f"🎙️ Cloning Request: {text[:30]}...")
    output_path = "output.wav"
    
    # ⚠️ Check if voice sample exists
    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Error: 'my_voice.wav' not found! Please upload your voice sample.", status_code=500)

    try:
        # 🔥 GENERATION
        # language='hi' use kar rahe hain kyunke XTTS Urdu ko Hindi engine ke through best bolta hai
        tts.tts_to_file(
            text=text,
            speaker_wav=SPEAKER_WAV,
            language="hi", 
            file_path=output_path
        )
        
        # Read & Return
        with open(output_path, "rb") as f:
            audio_data = f.read()
            
        return Response(content=audio_data, media_type="audio/wav")
        
    except Exception as e:
        print(f"❌ XTTS Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    # 8080 Port Lazmi hai Railway ke liye
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))