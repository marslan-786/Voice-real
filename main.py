import os
import uvicorn
import torch
import time
import gc
from fastapi import FastAPI, Form, Response
from TTS.api import TTS

# 🔥 FORCE 32 CORES & OPTIMIZATIONS
torch.set_num_threads(32)
os.environ["OMP_NUM_THREADS"] = "32"
os.environ["MKL_NUM_THREADS"] = "32"

print("⏳ Loading XTTS Model (High Quality)...")
try:
    # Model load
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    print("✅ Model Loaded!")
except Exception as e:
    print(f"❌ Load Error: {e}")
    exit(1)

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ Input Text: {text[:30]}...")
    
    # Sirf WAV file banegi ab
    output_path = f"out_{os.urandom(4).hex()}.wav"

    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Voice sample missing", status_code=500)

    try:
        # 🔥 GENERATION
        # Hindi script for Urdu pronunciation
        # split_sentences=False for better emotion flow
        tts.tts_to_file(
            text=text, 
            speaker_wav=SPEAKER_WAV, 
            language="hi", 
            file_path=output_path,
            split_sentences=False, 
            speed=1.1  
        )
        
        duration = time.time() - start_time
        print(f"✅ Generated in {duration:.2f}s")

        # 📤 Send Raw WAV to Go
        with open(output_path, "rb") as f:
            data = f.read()
        
        # Cleanup
        if os.path.exists(output_path): os.remove(output_path)
        gc.collect() # RAM Cleanup
        
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))