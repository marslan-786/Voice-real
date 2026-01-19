import os
import uvicorn
import sherpa_onnx
from fastapi import FastAPI, Form, Response
import time

print("⏳ Initializing Alibaba CosyVoice (Sherpa 1.10.16)...")

model_dir = "./model_data"
model_path = f"{model_dir}/model.onnx"
tokens_path = f"{model_dir}/tokens.txt"

if not os.path.exists(model_path):
    print("❌ Critical: Model file missing!")
    exit(1)

# 🔥 DIRECT CONFIGURATION (No Fancy Classes)
try:
    # 1.10.16 mein ye structure tha
    config = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            cosyvoice=sherpa_onnx.OfflineTtsCosyVoiceModelConfig(
                model=model_path,
            ),
        ),
        rule_fsts="", 
        max_num_sentences=1,
    )
    tts = sherpa_onnx.OfflineTts(config)
    print("✅ Engine Started Successfully (Standard Mode)!")

except AttributeError:
    print("⚠️ Standard Config Failed. Trying Raw Struct...")
    # AGAR STANDARD FAIL HO TO YEH CHALE GA
    # Hum config ko manually build kar rahe hain
    try:
        tts = sherpa_onnx.OfflineTts(
            config=sherpa_onnx.OfflineTtsConfig(
                model=sherpa_onnx.OfflineTtsModelConfig(
                    # Yahan hum VITS ke through load karne ki koshish karein ge (Hack)
                    # Kyunke kabhi kabhi internal mapping same hoti hai
                    vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                        model=model_path,
                        tokens=tokens_path,
                    ),
                )
            )
        )
        print("✅ Engine Started via VITS Hack!")
    except Exception as e2:
        print(f"❌ Both Methods Failed: {e2}")
        exit(1)

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.get("/")
def home():
    return {"status": "CosyVoice Running"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ Generating: {text[:20]}...")
    output_path = f"out_{os.urandom(4).hex()}.wav"

    if not os.path.exists(SPEAKER_WAV):
        return Response(content="Voice sample missing", status_code=500)

    try:
        audio = tts.generate(text, sid=0, speed=1.0)
        audio.save(output_path)
        
        print(f"✅ Done in {time.time() - start_time:.2f}s")
        
        with open(output_path, "rb") as f:
            data = f.read()
        os.remove(output_path)
        return Response(content=data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))