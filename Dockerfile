FROM python:3.10-slim

# ✅ Fast Logging
ENV PYTHONUNBUFFERED=1

# ✅ System Dependencies (Git & Git-LFS are CRITICAL here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git git-lfs curl ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

WORKDIR /app

# ✅ Python Libraries
RUN pip install --upgrade pip && \
    pip install --no-cache-dir sherpa-onnx fastapi uvicorn python-multipart

# ✅ DOWNLOAD ALIBABA COSYVOICE (via Git Clone)
# یہ Sherpa کا آفیشل کنورٹڈ ماڈل ہے جو 100٪ موجود ہے
# ہم اسے 'model_data' فولڈر میں کلون کر رہے ہیں
RUN git clone https://huggingface.co/csukuangfj/sherpa-onnx-tts-cosyvoice-300m-sft model_data \
    && rm -rf model_data/.git

# ⚠️ اپنی آواز کی فائل یہاں رکھیں (Cloning کے لیے)
COPY my_voice.wav .

COPY main.py .

CMD ["python", "main.py"]