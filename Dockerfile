FROM python:3.10-slim

# ✅ Fast Logging
ENV PYTHONUNBUFFERED=1

# ✅ Install System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential git curl tar ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Install Sherpa-ONNX (The Engine that runs Alibaba on CPU fast)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir sherpa-onnx fastapi uvicorn python-multipart

# ✅ Download Optimized Alibaba CosyVoice Model (300M)
# یہ Github Release سے ڈائریکٹ اٹھا رہا ہے (HuggingFace کا رولا نہیں)
RUN curl -L -o model.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/cosyvoice-300m-sft-partner.tar.bz2 \
    && tar -xvf model.tar.bz2 \
    && rm model.tar.bz2

# ماڈل کا فولڈر سیٹ کریں
RUN mv cosyvoice-300m-sft-partner model_data

COPY main.py .

# ⚠️ اپنی آواز کی فائل یہاں رکھنی ہے
COPY my_voice.wav .

CMD ["python", "main.py"]