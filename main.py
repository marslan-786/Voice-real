import os
import uvicorn
import torch
import time
import gc
import subprocess
from fastapi import FastAPI, Form, Response
from TTS.api import TTS

# 🔥 FORCE 32 CORES & OPTIMIZATIONS
torch.set_num_threads(32)
os.environ["OMP_NUM_THREADS"] = "32"
os.environ["MKL_NUM_THREADS"] = "32"

print("⏳ Loading XTTS Model (High Quality)...")
try:
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
    
    wav_path = f"temp_{os.urandom(4).hex()}.wav"
    ogg_path = f"out_{os.urandom(4).hex()}.ogg"

    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Voice sample missing", status_code=500)

    try:
        # 🔥 GENERATION TWEAKS
        # split_sentences=False (Emotion kill nahi hoga)
        # speed=1.1 (Thora tez bolega, natural lagega)
        tts.tts_to_file(
            text=text, 
            speaker_wav=SPEAKER_WAV, 
            language="hi", 
            file_path=wav_path,
            split_sentences=False, 
            speed=1.1  
        )
        
        # 🎵 CONVERT TO WHATSAPP FORMAT (OGG OPUS)
        # Yeh step file ko 'PTT' banata hai jo foran play hoti hai
        subprocess.run([
            "ffmpeg", "-y", "-i", wav_path, 
            "-c:a", "libopus", "-b:a", "64k", "-vbr", "on", "-compression_level", "10",
            ogg_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        duration = time.time() - start_time
        print(f"✅ Generated & Converted in {duration:.2f}s")

        with open(ogg_path, "rb") as f:
            data = f.read()
        
        # Cleanup
        if os.path.exists(wav_path): os.remove(wav_path)
        if os.path.exists(ogg_path): os.remove(ogg_path)
        gc.collect() # RAM Safai
        
        # Return proper OGG MIME type
        return Response(content=data, media_type="audio/ogg")

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))