# ✅ Using Python 3.10 (Most Stable for Coqui TTS)
FROM python:3.10-slim

# ✅ System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libsndfile1 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Upgrade pip
RUN pip install --upgrade pip

# ✅ Install Specific PyTorch (2.4.0) to avoid Security Error
# Yeh version Coqui TTS ke sath 100% compatible hai aur 'WeightsUnpickler' error nahi deta
RUN pip install --no-cache-dir torch==2.4.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cpu

# ✅ Install Coqui TTS (The Voice Cloning Beast)
RUN pip install --no-cache-dir tts

# ✅ Install API Server Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Accept Coqui License
ENV COQUI_TOS_AGREED=1

# Copy App Code
COPY main.py .

# ⚠️ Make sure 'my_voice.wav' is in your repo
COPY my_voice.wav . 

CMD ["python", "main.py"]