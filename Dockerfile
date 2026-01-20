FROM python:3.10-slim

# ✅ Fast Logs & Performance
ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=32
ENV MKL_NUM_THREADS=32
ENV TORCH_NUM_THREADS=32
ENV COQUI_TOS_AGREED=1

# ✅ Install System Dependencies (FFmpeg is HERE)
# یہ لائن FFmpeg کو سسٹم میں انسٹال کر رہی ہے 👇
RUN apt-get update && apt-get install -y \
    build-essential git curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip

# ✅ CRITICAL FIX 1: Pin PyTorch to 2.2.0 (Stable for Coqui)
RUN pip install --no-cache-dir torch==2.2.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cpu

# ✅ CRITICAL FIX 2: Pin Transformers (to avoid BeamSearchScorer error)
RUN pip install --no-cache-dir transformers==4.40.0

# ✅ Install Coqui TTS & API Server
RUN pip install --no-cache-dir tts fastapi uvicorn python-multipart

# ✅ PRE-DOWNLOAD MODEL
RUN python3 -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2').to('cpu')"

# ⚠️ Make sure my_voice.wav is present
COPY my_voice.wav .
COPY main.py .

CMD ["python", "main.py"]