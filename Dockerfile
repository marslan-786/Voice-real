FROM python:3.10-slim

# ✅ Logs will appear instantly
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential git libsndfile1 ffmpeg curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --upgrade pip

# ✅ Optimized PyTorch
RUN pip install --no-cache-dir torch==2.4.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir tts

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV COQUI_TOS_AGREED=1

COPY main.py .
COPY my_voice.wav . 

CMD ["python", "main.py"]