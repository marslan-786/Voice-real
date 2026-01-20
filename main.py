import os
import uvicorn
import torch
import time
from fastapi import FastAPI, Form, Response
from TTS.api import TTS

# 🔥 FORCE 32 CORES (Engine Turbo Mode)
torch.set_num_threads(32)
os.environ["OMP_NUM_THREADS"] = "32"
os.environ["MKL_NUM_THREADS"] = "32"

print(f"🚀 CPU Cores Detected: {os.cpu_count()}")
print(f"🔥 Active Threads set to: {torch.get_num_threads()}")

print("⏳ Loading XTTS v2 Model from Cache...")
# Model pehle se downloaded hai (Dockerfile ki waja se), foran load hoga
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
print("✅ Model Loaded Successfully!")

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.get("/")
def home():
    return {"status": "XTTS v2 Turbo Running", "cores": torch.get_num_threads()}

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ Generating: {text[:30]}...")
    
    output_path = f"out_{os.urandom(4).hex()}.wav"

    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Voice sample missing", status_code=500)

    try:
        # 🔥 GENERATION
        # language="ur" ya "hi" use karein best result ke liye
        tts.tts_to_file(
            text=text, 
            speaker_wav=SPEAKER_WAV, 
            language="ur", 
            file_path=output_path
        )
        
        duration = time.time() - start_time
        print(f"✅ Generated in {duration:.2f}s using 32 Cores")

        with open(output_path, "rb") as f:
            data = f.read()
        
        os.remove(output_path)
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))