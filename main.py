import os
import uvicorn
import sherpa_onnx
from fastapi import FastAPI, Form, Response
import time

print("⏳ Initializing Alibaba CosyVoice (Sherpa Engine)...")

# ⚙️ MODEL PATH
model_dir = "./model_data"
model_path = f"{model_dir}/model.onnx"
tokens_path = f"{model_dir}/tokens.txt"

# ✅ Verification Check
if not os.path.exists(model_path):
    print(f"❌ CRITICAL ERROR: {model_path} not found!")
    exit(1)

# 🔥 FIXED CONFIGURATION (The Generic Way)
# Bajaye specific class use karne ke, hum direct model path set kar rahe hain
tts_config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        cosyvoice=sherpa_onnx.OfflineTtsCosyVoiceModelConfig(
            model=model_path,
        ),
    ),
    rule_fsts="", 
    max_num_sentences=1,
)

# 🛑 AGAR UPAR WALA CODE FAIL HO TO YEH TRY KAREIN (Commented out for now)
# tts_config.model.cosyvoice.model = model_path

# 🚀 LOAD ENGINE
try:
    tts = sherpa_onnx.OfflineTts(tts_config)
    print("✅ Alibaba CosyVoice Engine Started Successfully!")
except AttributeError:
    # ⚠️ FALLBACK FOR OLDER SHERPA VERSIONS
    print("⚠️ Detect older Sherpa version. Trying VITS configuration...")
    tts_config = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=model_path,
                tokens=tokens_path,
            ),
        ),
    )
    tts = sherpa_onnx.OfflineTts(tts_config)
    print("✅ Engine Started in VITS Mode (Compatible)!")

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
        return Response(content="Voice sample missing", status_code=500)

    try:
        # 🔥 GENERATION
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