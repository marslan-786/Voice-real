import os
import uvicorn
from fastapi import FastAPI, Form, Response
from melo.api import TTS

# 🚀 Pre-load Model on Startup
print("⏳ Initializing MeloTTS (Might download assets on first run)...")
device = 'cpu'
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id

app = FastAPI()

@app.get("/")
def home():
    return {"status": "MeloTTS Voice Server Running 🚀"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    print(f"🎙️ Generating: {text[:20]}...")
    output_path = "output.wav"
    
    try:
        # EN-India accent handles Urdu nuance best
        model.tts_to_file(text, speaker_ids['EN-India'], output_path, speed=1.0)
        
        with open(output_path, "rb") as f:
            audio_data = f.read()
            
        return Response(content=audio_data, media_type="audio/wav")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))