FROM python:3.10-slim

# ✅ Fast Logs & Performance
ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=32
ENV MKL_NUM_THREADS=32
ENV TORCH_NUM_THREADS=32
ENV COQUI_TOS_AGREED=1

# ✅ Install System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential git curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip

# ✅ CRITICAL FIX 1: Pin PyTorch to 2.2.0 (Stable for Coqui)
# Naya version (2.4+) security error deta hai, isliye hum purana stable version use karenge
RUN pip install --no-cache-dir torch==2.2.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cpu

# ✅ CRITICAL FIX 2: Pin Transformers
RUN pip install --no-cache-dir transformers==4.40.0

# ✅ Install Coqui TTS
RUN pip install --no-cache-dir tts fastapi uvicorn python-multipart

# ✅ PRE-DOWNLOAD MODEL (Ab yeh fail nahi hoga)
RUN python3 -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2').to('cpu')"

# ⚠️ Make sure my_voice.wav is present in Project B folder
COPY my_voice.wav .
COPY main.py .

CMD ["python", "main.py"]