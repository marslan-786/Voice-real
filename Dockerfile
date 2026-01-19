# ✅ Using Python 3.11 (Latest Stable for AI)
FROM python:3.11-slim

# ✅ System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    git-lfs \
    libsndfile1 \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Upgrade pip
RUN pip install --upgrade pip

# ✅ Install Core AI Libraries
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# ✅ Install MeloTTS Directly from GitHub
RUN pip install --no-cache-dir git+https://github.com/myshell-ai/MeloTTS.git

# ✅ Install Other Requirements
COPY requirements.txt .
# Remove 'melo-tts' from requirements.txt to avoid conflict
RUN sed -i '/melo-tts/d' requirements.txt && pip install --no-cache-dir -r requirements.txt

# ❌ REMOVED: "RUN python3 -m unidic_lite.download" (یہ لائن ایرر دے رہی تھی، ہٹا دی ہے)

# Copy Application Code
COPY main.py .

CMD ["python", "main.py"]