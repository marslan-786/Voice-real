FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Install Specific Stable Version (1.10.45)
# Yeh version PyPI par mojood hai aur CosyVoice support karta hai
RUN pip install --upgrade pip && \
    pip install --no-cache-dir sherpa-onnx==1.10.45 fastapi uvicorn python-multipart

# ✅ DOWNLOAD MODEL (Direct Curl)
RUN mkdir -p model_data
RUN curl -L -o model_data/model.onnx "https://huggingface.co/csukuangfj/sherpa-onnx-tts-cosyvoice-300m-sft/resolve/main/model.onnx"
RUN curl -L -o model_data/tokens.txt "https://huggingface.co/csukuangfj/sherpa-onnx-tts-cosyvoice-300m-sft/resolve/main/tokens.txt"

COPY my_voice.wav .
COPY main.py .

CMD ["python", "main.py"]