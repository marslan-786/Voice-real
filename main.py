import os
import uvicorn
import torch
import time
import gc
from fastapi import FastAPI, Form, Response
from TTS.api import TTS

# 🔥 OPTIMIZED THREADS (32 is too much overhead, 16 is sweet spot)
torch.set_num_threads(16)
os.environ["OMP_NUM_THREADS"] = "16"
os.environ["MKL_NUM_THREADS"] = "16"

print(f"🚀 System CPU Cores: {os.cpu_count()}")
print(f"🔥 Active Threads: {torch.get_num_threads()}")

# ✅ LOAD MODEL ONCE (Global Variable)
print("⏳ Loading XTTS Model into RAM...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
print("✅ Model Ready & Locked in RAM!")

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ New Request: {text[:30]}...")
    
    output_path = f"out_{os.urandom(4).hex()}.wav"

    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Voice sample missing", status_code=500)

    try:
        # 🔥 GENERATION (No Reloading)
        tts.tts_to_file(
            text=text, 
            speaker_wav=SPEAKER_WAV, 
            language="hi", 
            file_path=output_path,
            split_sentences=True # Sentences todne se memory kam use hogi
        )
        
        duration = time.time() - start_time
        print(f"✅ Generated in {duration:.2f}s")

        with open(output_path, "rb") as f:
            data = f.read()
        
        os.remove(output_path)

        # 🧹 CLEANUP MEMORY (Crucial Step)
        gc.collect()
        
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))