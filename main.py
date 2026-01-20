import os
import uvicorn
import torch
import time
import gc
from fastapi import FastAPI, Form, Response
from TTS.api import TTS

# 🔥 PERFORMANCE TUNING (The Real Fix)
# 32 Threads causing deadlock/hangs on 2nd request.
# 8 Threads is the sweet spot for fastest CPU Inference.
NUM_THREADS = "8"
os.environ["OMP_NUM_THREADS"] = NUM_THREADS
os.environ["MKL_NUM_THREADS"] = NUM_THREADS
torch.set_num_threads(int(NUM_THREADS))

print(f"🚀 Optimized Configuration: {NUM_THREADS} Active Threads (Preventing Deadlock)")

print("⏳ Loading XTTS Model...")
try:
    # Model Load
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    print("✅ Model Loaded & Ready!")
except Exception as e:
    print(f"❌ Load Error: {e}")
    exit(1)

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ Generating: {text[:30]}...")
    
    output_path = f"out_{os.urandom(4).hex()}.wav"

    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Voice sample missing", status_code=500)

    try:
        # 🔥 GENERATION
        # split_sentences=False (Flow acha rahega)
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

        with open(output_path, "rb") as f:
            data = f.read()
        
        # Cleanup
        if os.path.exists(output_path): os.remove(output_path)
        
        # 🧹 AGGRESSIVE RAM CLEANUP
        gc.collect()
        
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))