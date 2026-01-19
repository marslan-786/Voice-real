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

# ✅ Install MeloTTS Directly
RUN pip install --no-cache-dir git+https://github.com/myshell-ai/MeloTTS.git

# ✅ Fix MeCab (Japanese Dictionary)
RUN pip install --no-cache-dir unidic
RUN python -m unidic download

# ✅ Install Other Requirements
COPY requirements.txt .
RUN sed -i '/melo-tts/d' requirements.txt && pip install --no-cache-dir -r requirements.txt

# 🔥 CRITICAL FIX: Download NLTK Data (The Missing Brain Cells)
# یہ لائن وہ ڈیٹا ڈاؤن لوڈ کرے گی جس کی وجہ سے ایرر آ رہا تھا
RUN python -m nltk.downloader -d /usr/local/share/nltk_data averaged_perceptron_tagger_eng averaged_perceptron_tagger cmudict punkt

# Copy App Code
COPY main.py .

CMD ["python", "main.py"]