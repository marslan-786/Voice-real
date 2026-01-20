FROM python:3.10-slim

# ✅ Fast Logs
ENV PYTHONUNBUFFERED=1

# ✅ Install System Tools (Git & FFmpeg are must)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ 1. Install PyTorch (CPU Version - Lightweight)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# ✅ 2. Install MeloTTS (Direct form GitHub)
# Hum isay direct install kar rahay hain taakay dependencies khud handle ho jayen
RUN pip install git+https://github.com/myshell-ai/MeloTTS.git

# ✅ 3. Download Dictionary (Required by MeloTTS to start)
RUN python -m unidic download

# ✅ Install Server dependencies
RUN pip install fastapi uvicorn python-multipart

COPY main.py .

CMD ["python", "main.py"]