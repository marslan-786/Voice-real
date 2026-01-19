# ✅ Using Python 3.11 (Latest Stable for AI)
FROM python:3.11-slim

# ✅ System Dependencies (MeloTTS needs these heavy tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    git-lfs \
    libsndfile1 \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Upgrade pip to latest
RUN pip install --upgrade pip

# ✅ Install Core AI Libraries First (To prevent conflicts)
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# ✅ Install MeloTTS Directly from GitHub (Kyunk pip par kabhi kabhi issue ata hai)
RUN pip install --no-cache-dir git+https://github.com/myshell-ai/MeloTTS.git

# ✅ Install Other Requirements
COPY requirements.txt .
# Remove 'melo-tts' from requirements.txt via sed command just in case, because we installed it above
RUN sed -i '/melo-tts/d' requirements.txt && pip install --no-cache-dir -r requirements.txt

# ✅ Download Language Dictionary (Crucial for MeloTTS)
RUN python3 -m unidic_lite.download

# Copy Application Code
COPY main.py .

CMD ["python", "main.py"]