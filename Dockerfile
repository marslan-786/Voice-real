FROM python:3.10-slim

# ✅ Logs Fast Aayen
ENV PYTHONUNBUFFERED=1

# ✅ Unlock FULL CPU POWER (32 Cores)
ENV OMP_NUM_THREADS=32
ENV MKL_NUM_THREADS=32
ENV TORCH_NUM_THREADS=32
ENV COQUI_TOS_AGREED=1

# ✅ Install System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential git curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Install Python & PyTorch (CPU)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# ✅ CRITICAL FIX: Pin Transformers to 4.40.0 BEFORE installing TTS
# Naya version XTTS ko crash kar deta hai
RUN pip install --no-cache-dir transformers==4.40.0

# ✅ Install Coqui TTS & Server
RUN pip install --no-cache-dir tts fastapi uvicorn python-multipart

# ✅ PRE-DOWNLOAD MODEL
# Ab yeh crash nahi karega kyunke transformers version match ho gaya hai
RUN python3 -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2').to('cpu')"

# ⚠️ Copy Voice File
COPY my_voice.wav .
COPY main.py .

CMD ["python", "main.py"]