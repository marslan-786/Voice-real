import os
import uvicorn
from fastapi import FastAPI, Form, Response
from melo.api import TTS

print("⏳ Initializing MeloTTS...")
device = 'cpu'
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id

# 🔍 DEBUG: Print available speakers to Console
print("\n🎤 AVAILABLE SPEAKERS:", speaker_ids)
print("--------------------------------------\n")

app = FastAPI()

@app.get("/")
def home():
    return {"status": "MeloTTS Running", "speakers": str(speaker_ids)}

@app.post("/speak")
async def speak(text: str = Form(...)):
    print(f"🎙️ Generating: {text[:20]}...")
    output_path = "output.wav"
    
    try:
        # 🧠 SMART SPEAKER SELECTION
        # پہلے 'EN-India' ڈھونڈو، اگر نہ ملے تو 'EN-US'، وہ بھی نہ ملے تو لسٹ کا پہلا والا اٹھا لو
        
        # Note: speaker_ids might be a Dict or HParams object
        spk_dict = dict(speaker_ids) # Safe convert to dict
        
        selected_speaker = spk_dict.get('EN-India')
        if selected_speaker is None:
            selected_speaker = spk_dict.get('EN_India') # Try with underscore
        if selected_speaker is None:
            selected_speaker = spk_dict.get('EN-US') # Fallback to US
        if selected_speaker is None:
            # Absolute fallback: Pick the first available key
            first_key = list(spk_dict.keys())[0]
            selected_speaker = spk_dict[first_key]
            print(f"⚠️ 'EN-India' not found. Using fallback: {first_key}")

        # Generate Audio
        model.tts_to_file(text, selected_speaker, output_path, speed=1.0)
        
        with open(output_path, "rb") as f:
            audio_data = f.read()
            
        return Response(content=audio_data, media_type="audio/wav")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))