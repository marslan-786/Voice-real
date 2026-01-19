import os
import uvicorn
import time
from fastapi import FastAPI, Form, Response
import torch
# ✅ Fix for Security Error
torch.serialization.add_safe_globals = lambda *args, **kwargs: None 
from TTS.api import TTS

# 🚀 FORCE CPU POWER (32 Cores Use Karo!)
torch.set_num_threads(32)
print(f"🔥 CPU Threads set to: {torch.get_num_threads()}")

print("⏳ Loading XTTS v2 Model...")
start_load = time.time()
device = "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
print(f"✅ Model Loaded in {time.time() - start_load:.2f} seconds!")

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.get("/")
def home():
    return {"status": "XTTS Ready", "threads": torch.get_num_threads()}

@app.post("/speak")
async def speak(text: str = Form(...)):
    print(f"\n📨 Received Request: '{text[:20]}...'")
    
    if not os.path.exists(SPEAKER_WAV):
        print("❌ Error: my_voice.wav not found!")
        return Response(content="Voice sample missing", status_code=500)

    output_path = f"output_{os.urandom(4).hex()}.wav"
    
    try:
        start_gen = time.time()
        print("⚙️ Processing Started...")
        
        # 🔥 GENERATION
        tts.tts_to_file(
            text=text,
            speaker_wav=SPEAKER_WAV,
            language="hi", # Hindi/Urdu
            file_path=output_path
        )
        
        duration = time.time() - start_gen
        print(f"✅ Audio Generated in {duration:.2f} seconds!")
        
        with open(output_path, "rb") as f:
            audio_data = f.read()
            
        os.remove(output_path) # Cleanup
        return Response(content=audio_data, media_type="audio/wav")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))