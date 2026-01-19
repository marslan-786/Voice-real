# ✅ Python 3.10 is most stable for Coqui TTS
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

# ✅ Install PyTorch first (CPU Version)
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# ✅ Install Coqui TTS (The Voice Cloning Beast)
# ہم اس کا مخصوص ورژن انسٹال کر رہے ہیں جو سٹیبل ہے
RUN pip install --no-cache-dir tts

# ✅ Install API Server Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Accept Coqui License (Environment Variable)
ENV COQUI_TOS_AGREED=1

# Copy App Code
COPY main.py .

# ⚠️ IMPORTANT: Aapki awaaz ka sample yahan hona chahiye
# Agar nahi hai to code default use karega ya error dega.
# Behtar hai ke aap 'my_voice.wav' project mein upload karein.
COPY male_voice.wav . 

CMD ["python", "main.py"]