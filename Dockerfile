FROM python:3.10-slim

# ✅ Logs Fast Aayen
ENV PYTHONUNBUFFERED=1

# ✅ Unlock FULL CPU POWER (32 Cores)
# Yeh variables Python ko majboor karte hain ke saray cores use kare
ENV OMP_NUM_THREADS=32
ENV MKL_NUM_THREADS=32
ENV TORCH_NUM_THREADS=32
ENV COQUI_TOS_AGREED=1

# ✅ Install System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential git curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Install PyTorch & Coqui TTS
RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir tts fastapi uvicorn python-multipart

# ✅ PRE-DOWNLOAD MODEL (Taakay runtime par wait na karna pare)
# Hum container banate waqt hi model download kar rahay hain
RUN python3 -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2').to('cpu')"

# ⚠️ Copy Voice File
COPY my_voice.wav .
COPY main.py .

CMD ["python", "main.py"]