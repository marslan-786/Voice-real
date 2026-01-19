import os
import uvicorn
from fastapi import FastAPI, Form, Response
from melo.api import TTS

# 🚀 Initialize MeloTTS
# 'EN' language does NOT use MeCab, so it's safe
print("⏳ Initializing MeloTTS (EN Mode)...")
try:
    device = 'cpu'
    model = TTS(language='EN', device=device)
    speaker_ids = model.hps.data.spk2id
    print("✅ MeloTTS Loaded Successfully!")
except Exception as e:
    print(f"❌ Init Error: {e}")
    exit(1)

app = FastAPI()

@app.get("/")
def home():
    return {"status": "MeloTTS Running"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    print(f"🎙️ Speaking: {text[:20]}...")
    output_path = f"out_{os.urandom(4).hex()}.wav"

    try:
        # EN-India accent sounds very close to Urdu/Hindi
        # Speed 1.0 is normal
        speaker_key = 'EN-India'
        if speaker_key not in speaker_ids:
             speaker_key = 'EN_INDIA' # Try alternate casing
        
        if speaker_key not in speaker_ids:
             speaker_key = 'EN-US' # Fallback
             
        model.tts_to_file(text, speaker_ids[speaker_key], output_path, speed=1.0)
        
        with open(output_path, "rb") as f:
            data = f.read()
        os.remove(output_path)
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Generation Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))