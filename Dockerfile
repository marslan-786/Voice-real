FROM python:3.10-slim

# ✅ Fast Logging
ENV PYTHONUNBUFFERED=1

# ✅ Install System Dependencies & Git LFS
# git-lfs is mandatory for downloading large AI models
RUN apt-get update && apt-get install -y \
    build-essential git git-lfs curl tar ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

WORKDIR /app

# ✅ Install Sherpa-ONNX
RUN pip install --upgrade pip
RUN pip install --no-cache-dir sherpa-onnx fastapi uvicorn python-multipart

# ✅ Download Model via GIT CLONE (The Most Reliable Way)
# ہم ڈائریکٹ Sherpa کے ڈویلپر کی ریپو کلون کر رہے ہیں، لنک ٹوٹنے کا چانس 0٪ ہے
RUN git clone https://huggingface.co/csukuangfj/sherpa-onnx-tts-cosyvoice-300m-sft-partner model_data

# Cleanup hidden git folder to save space
RUN rm -rf model_data/.git

COPY main.py .

# ⚠️ Make sure your voice sample is here
COPY my_voice.wav .

CMD ["python", "main.py"]