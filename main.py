import os
import uvicorn
import torch
import time
import gc
from fastapi import FastAPI, Form, Response
from TTS.api import TTS

# ... (Thread settings same as before) ...

print("⏳ Loading XTTS Model...")
try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    print("✅ Model Loaded!")
except Exception as e:
    print(f"❌ Load Error: {e}")
    exit(1)

app = FastAPI()

# Default fallback voice
DEFAULT_VOICE = "voice_1.wav"

@app.post("/speak")
async def speak(text: str = Form(...), speaker: str = Form(DEFAULT_VOICE)):
    start_time = time.time()
    
    # ✅ Check if requested voice exists, else use default
    target_voice = speaker if os.path.exists(speaker) else DEFAULT_VOICE
    
    print(f"🎙️ Generating: {text[:20]}... | 🗣️ Voice: {target_voice}")
    
    output_path = f"out_{os.urandom(4).hex()}.wav"

    try:
        # 🔥 GENERATION
        tts.tts_to_file(
            text=text, 
            speaker_wav=target_voice, # 👈 Dynamic Voice Here
            language="hi", 
            file_path=output_path,
            split_sentences=False, 
            speed=1.0,
            temperature=0.8
        )
        
        # ... (File sending and cleanup code same as before) ...
        
        with open(output_path, "rb") as f:
            data = f.read()
        
        if os.path.exists(output_path): os.remove(output_path)
        gc.collect()
        
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)