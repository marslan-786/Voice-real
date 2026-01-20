import os
import uvicorn
import torch
import time
import gc
from fastapi import FastAPI, Form, Response
from TTS.api import TTS

# 🔥 THREADS SETTING (8 for Stability)
NUM_THREADS = "8"
os.environ["OMP_NUM_THREADS"] = NUM_THREADS
os.environ["MKL_NUM_THREADS"] = NUM_THREADS
torch.set_num_threads(int(NUM_THREADS))

print("⏳ Loading XTTS Model...")
try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    print("✅ Model Loaded!")
except Exception as e:
    print(f"❌ Load Error: {e}")
    exit(1)

app = FastAPI()
SPEAKER_WAV = "my_voice.wav" # Default Fallback

# ✅✅✅ NEW HEALTH CHECK ROUTE (Fixes 404 Error) ✅✅✅
@app.get("/")
def home():
    return {"status": "alive", "message": "XTTS Server is Ready!"}

@app.post("/speak")
async def speak(text: str = Form(...), speaker: str = Form(SPEAKER_WAV)):
    start_time = time.time()
    
    # Check if requested voice exists
    target_voice = speaker if os.path.exists(speaker) else SPEAKER_WAV
    print(f"🎙️ Generating: {text[:20]}... | 🗣️ Voice: {target_voice}")
    
    output_path = f"out_{os.urandom(4).hex()}.wav"

    try:
        # 🔥 GENERATION
        tts.tts_to_file(
            text=text, 
            speaker_wav=target_voice,
            language="hi", 
            file_path=output_path,
            split_sentences=False, 
            speed=1.0,
            temperature=0.8
        )
        
        duration = time.time() - start_time
        print(f"✅ Generated in {duration:.2f}s")

        with open(output_path, "rb") as f:
            data = f.read()
        
        if os.path.exists(output_path): os.remove(output_path)
        gc.collect()
        
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

# ✅ AUDIO TRANSCRIPTION (Whisper Support if needed)
@app.post("/transcribe")
async def transcribe(file: bytes = Form(...)):
    # Yahan agar aap ne Whisper lagaya hai to uska code ayega
    # Filhal dummy return kar raha hu taakay error na aye
    return {"text": "Transcription feature pending implementation."}

if __name__ == "__main__":
    # 0.0.0.0 is Must for Docker/Railway
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))