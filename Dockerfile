FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Force Latest Version of Sherpa-ONNX
RUN pip install --upgrade pip && \
    pip install --no-cache-dir sherpa-onnx>=1.10.16 fastapi uvicorn python-multipart

# ✅ DOWNLOAD MODEL
RUN mkdir -p model_data
RUN curl -L -o model_data/model.onnx "https://huggingface.co/csukuangfj/sherpa-onnx-tts-cosyvoice-300m-sft/resolve/main/model.onnx"
RUN curl -L -o model_data/tokens.txt "https://huggingface.co/csukuangfj/sherpa-onnx-tts-cosyvoice-300m-sft/resolve/main/tokens.txt"

COPY my_voice.wav .
COPY main.py .

CMD ["python", "main.py"]