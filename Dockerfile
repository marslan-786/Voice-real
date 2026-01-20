FROM python:3.10-slim

# ✅ Fast Logs
ENV PYTHONUNBUFFERED=1

# 🔥 PERFORMANCE TUNING (Fixed to 8 for Stability)
# 32 Threads CPU ko 'choke' kar dete hain, 8 best speed dete hain.
ENV OMP_NUM_THREADS=8
ENV MKL_NUM_THREADS=8
ENV TORCH_NUM_THREADS=8
ENV COQUI_TOS_AGREED=1

# ✅ Install System Dependencies
# FFmpeg zaroori hai agar hum kabhi conversion karein
RUN apt-get update && apt-get install -y \
    build-essential git curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip

# ✅ Pin PyTorch to Stable Version (Security Warning Bypass)
RUN pip install --no-cache-dir torch==2.2.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cpu

# ✅ Pin Transformers
RUN pip install --no-cache-dir transformers==4.40.0

# ✅ Install Coqui TTS & Server
RUN pip install --no-cache-dir tts fastapi uvicorn python-multipart

# ✅ PRE-DOWNLOAD MODEL
RUN python3 -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2').to('cpu')"

# ⚠️ Copy Voice File (Make sure updated wav file is here)
COPY *.wav .
COPY main.py .

CMD ["python", "main.py"]