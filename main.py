import os
import uvicorn
from fastapi import FastAPI, Form, Response
# MeloTTS Imports
from melo.api import TTS

print("⏳ Initializing MeloTTS (CPU Mode)...")

try:
    # 'EN' language use kar rahay hain (No MeCab issues)
    # Device 'cpu' hai (Railway friendly)
    model = TTS(language='EN', device='cpu')
    speaker_ids = model.hps.data.spk2id
    print("✅ MeloTTS Engine Started Successfully!")
except Exception as e:
    print(f"❌ Initialization Error: {e}")
    exit(1)

app = FastAPI()

@app.get("/")
def home():
    return {"status": "MeloTTS Running 🚀"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ Generating: {text[:30]}...")
    
    output_path = f"out_{os.urandom(4).hex()}.wav"

    try:
        # 🔥 TRICK: Use 'EN-India' accent for Urdu/Hindi feel
        # Agar 'EN-India' nahi mila to default 'EN-US' use hoga
        speaker_key = 'EN-India'
        if speaker_key not in speaker_ids:
            speaker_key = 'EN-Default'
            
        speaker_id = speaker_ids[speaker_key]
        
        # Generation
        model.tts_to_file(text, speaker_id, output_path, speed=1.0)
        
        # Read & Send
        with open(output_path, "rb") as f:
            audio_data = f.read()
        
        os.remove(output_path)
        return Response(content=audio_data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Generation Error: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return Response(content=str(e), status_code=500)

import time # Forgot to import time above

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)