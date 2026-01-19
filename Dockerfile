FROM python:3.10-slim

# ✅ Fast Logging
ENV PYTHONUNBUFFERED=1

# ✅ Install System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Install Python Libraries
RUN pip install --upgrade pip && \
    pip install --no-cache-dir sherpa-onnx fastapi uvicorn python-multipart

# ✅ DOWNLOAD MODEL FILES DIRECTLY (No Git Needed)
# ہم ماڈل کا فولڈر بنا رہے ہیں
RUN mkdir -p model_data

# 1. Download Model (180MB approx - SFT 300M)
RUN curl -L -o model_data/model.onnx "https://huggingface.co/csukuangfj/sherpa-onnx-tts-cosyvoice-300m-sft/resolve/main/model.onnx"

# 2. Download Tokens (Required for text processing)
RUN curl -L -o model_data/tokens.txt "https://huggingface.co/csukuangfj/sherpa-onnx-tts-cosyvoice-300m-sft/resolve/main/tokens.txt"

# ⚠️ Copy your voice file
COPY my_voice.wav .

COPY main.py .

CMD ["python", "main.py"]