import os
import uvicorn
import sherpa_onnx
from fastapi import FastAPI, Form, Response
import time

print("⏳ Initializing Alibaba CosyVoice (Universal Mode)...")

model_dir = "./model_data"
model_path = f"{model_dir}/model.onnx"
tokens_path = f"{model_dir}/tokens.txt"

if not os.path.exists(model_path):
    print("❌ CRITICAL: Model file missing!")
    exit(1)

# 🔥 UNIVERSAL LOADER (VITS Style)
# Yeh har Sherpa version par chalta hai, chahe woh naya ho ya purana
try:
    config = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=model_path,
                lexicon="",
                tokens=tokens_path,
            ),
        ),
        rule_fsts="", 
        max_num_sentences=1,
    )
    
    tts = sherpa_onnx.OfflineTts(config)
    print("✅ Engine Started Successfully (Universal VITS Mode)!")

except Exception as e:
    print(f"❌ Engine Crash: {e}")
    # Last attempt: Raw Dictionary
    try:
        print("⚠️ Trying Raw Dictionary Config...")
        tts = sherpa_onnx.OfflineTts(
            config={
                "model": {
                    "vits": {
                        "model": model_path,
                        "tokens": tokens_path,
                    }
                }
            }
        )
        print("✅ Raw Engine Started!")
    except Exception as e2:
        print(f"❌ Fatal Error: {e2}")
        exit(1)

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.get("/")
def home():
    return {"status": "CosyVoice (Universal) Running 🚀"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ Generating: {text[:20]}...")
    output_path = f"out_{os.urandom(4).hex()}.wav"

    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Voice sample missing", status_code=500)

    try:
        # sid=0 (Auto Speaker)
        audio = tts.generate(text, sid=0, speed=1.0)
        
        if len(audio.samples) == 0:
             return Response(content="Empty Audio", status_code=500)
             
        audio.save(output_path)
        
        print(f"✅ Generated in {time.time() - start_time:.2f}s")
        
        with open(output_path, "rb") as f:
            data = f.read()
        os.remove(output_path)
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Generation Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))