FROM python:3.10-slim

# ✅ Fast Logging
ENV PYTHONUNBUFFERED=1

# ✅ Install System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential git curl tar ffmpeg bzip2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Install Sherpa-ONNX
RUN pip install --upgrade pip
RUN pip install --no-cache-dir sherpa-onnx fastapi uvicorn python-multipart

# ✅ Download Model (FIXED LINK)
# ہم اس بار ماڈل کو Github کے "releases/download" والے پکے لنک سے اٹھا رہے ہیں
RUN curl -L -o model.tar.bz2 "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/cosyvoice-300m-sft-partner.tar.bz2" \
    && tar -xvf model.tar.bz2 \
    && rm model.tar.bz2

# ماڈل کا فولڈر سیٹ کریں
RUN mv cosyvoice-300m-sft-partner model_data

COPY main.py .

# ⚠️ اپنی آواز کی فائل یہاں رکھنی ہے (my_voice.wav)
COPY my_voice.wav .

CMD ["python", "main.py"]