# ✅ Python 3.11 (Sweet spot for AI)
FROM python:3.11-slim

# ✅ System Deps
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

# ✅ Install MeloTTS Directly
RUN pip install --no-cache-dir git+https://github.com/myshell-ai/MeloTTS.git

# ✅ CRITICAL FIX FOR MECAB (The Japanese Error)
# unidic lite kafi nahi tha, isliye full unidic download kar rahe hain
RUN pip install --no-cache-dir unidic
RUN python -m unidic download

# ✅ Install Other Requirements
COPY requirements.txt .
# Remove conflict causing packages
RUN sed -i '/melo-tts/d' requirements.txt && pip install --no-cache-dir -r requirements.txt

# Copy App Code
COPY main.py .

CMD ["python", "main.py"]