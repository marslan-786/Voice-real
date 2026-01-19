import os
import uvicorn
import sherpa_onnx
from fastapi import FastAPI, Form, Response
import time

print("⏳ Initializing Alibaba CosyVoice (Sherpa Engine)...")

# ⚙️ MODEL PATH CONFIGURATION
# Hugging Face Clone se ye files ayengi:
model_dir = "./model_data"

# Check files exist (Debugging)
if not os.path.exists(f"{model_dir}/model.onnx"):
    print("❌ CRITICAL: model.onnx not found! Git clone failed.")
    exit(1)

config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        cosyvoice=sherpa_onnx.OfflineTtsCosyVoiceModelConfig(
            model=f"{model_dir}/model.onnx", # Main Model
        ),
    ),
    # CosyVoice ke liye tokens.txt zaroori hota hai
    rule_fsts="", 
    max_num_sentences=1,
)
# Note: Sherpa automatically looks for 'tokens.txt' in the same dir as model.onnx

# 🚀 LOAD ENGINE
try:
    tts = sherpa_onnx.OfflineTts(config)
    print("✅ Alibaba CosyVoice Engine Started Successfully!")
except Exception as e:
    print(f"❌ Engine Start Error: {e}")
    exit(1)

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.get("/")
def home():
    return {"status": "CosyVoice Running 🚀"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ Generating for: {text[:20]}...")
    
    output_path = f"generated_{os.urandom(4).hex()}.wav"

    if not os.path.exists(SPEAKER_WAV):
        print("❌ my_voice.wav missing!")
        return Response(content="Voice sample missing", status_code=500)

    try:
        # 🔥 GENERATION
        # sid=0 (Auto/Single Speaker from Wav)
        audio = tts.generate(text, sid=0, speed=1.0)
        
        if len(audio.samples) == 0:
             return Response(content="Empty Audio", status_code=500)
             
        audio.save(output_path)
        
        duration = time.time() - start_time
        print(f"✅ Generated in {duration:.2f}s")

        with open(output_path, "rb") as f:
            audio_data = f.read()
        
        os.remove(output_path)
        return Response(content=audio_data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Generation Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))