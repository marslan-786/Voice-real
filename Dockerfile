FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential git curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Install Pure Python Dependencies (No complex C++ engines)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi uvicorn python-multipart torch torchaudio

# ✅ Install MeloTTS (Direct form GitHub but WITHOUT MeCab dependency manually)
# Hum MeloTTS ka code clone kar ke usay 'lite' mode mein chalayen ge
RUN git clone https://github.com/myshell-ai/MeloTTS.git
WORKDIR /app/MeloTTS
RUN pip install -e .
RUN python -m unidic download 

WORKDIR /app
COPY main.py .

CMD ["python", "main.py"]