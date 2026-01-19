import os
import uvicorn
import sherpa_onnx
from fastapi import FastAPI, Form, Response
import time

print("⏳ Initializing Alibaba CosyVoice (via Sherpa-ONNX)...")

# ⚙️ MODEL CONFIGURATION
# Hugging Face Repo se file ka naam 'model.onnx' hota hai
model_dir = "./model_data"
config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        cosyvoice=sherpa_onnx.OfflineTtsCosyVoiceModelConfig(
            model=f"{model_dir}/model.onnx", # ✅ Corrected Name
        ),
    ),
    rule_fsts=f"{model_dir}/date.fst,{model_dir}/phone.fst",
    max_num_sentences=1,
)

# 🚀 LOAD ENGINE
try:
    tts = sherpa_onnx.OfflineTts(config)
    print("✅ Alibaba CosyVoice Engine Started Successfully!")
except Exception as e:
    print(f"❌ Engine Start Error: {e}")
    # Agar error aye to exit karo takay logs mein nazar aye
    exit(1)

app = FastAPI()
SPEAKER_WAV = "my_voice.wav"

@app.get("/")
def home():
    return {"status": "Alibaba CosyVoice Running 🚀"}

@app.post("/speak")
async def speak(text: str = Form(...)):
    start_time = time.time()
    print(f"🎙️ Generating for: {text[:20]}...")
    
    output_path = f"generated_{os.urandom(4).hex()}.wav"

    if not os.path.exists(SPEAKER_WAV):
        print("❌ my_voice.wav NOT FOUND!")
        return Response(content="Error: my_voice.wav not found!", status_code=500)

    try:
        # 🔥 GENERATION COMMAND
        # sid=0 means auto-detect language based on text
        audio = tts.generate(text, sid=0, speed=1.0)
        
        if len(audio.samples) == 0:
             print("❌ Sherpa generated 0 bytes audio")
             return Response(content="Empty Audio Generated", status_code=500)
             
        audio.save(output_path)
        
        duration = time.time() - start_time
        print(f"✅ Generated in {duration:.2f} seconds!")

        with open(output_path, "rb") as f:
            audio_data = f.read()
        
        os.remove(output_path)
        return Response(content=audio_data, media_type="audio/wav")

    except Exception as e:
        print(f"❌ Generation Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))