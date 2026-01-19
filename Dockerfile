FROM python:3.10-slim

# ✅ Fast Logging
ENV PYTHONUNBUFFERED=1

# ✅ Install System Dependencies
# 'git-lfs' is critical
RUN apt-get update && apt-get install -y \
    build-essential git git-lfs curl ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

WORKDIR /app

# ✅ Install Python Libraries
RUN pip install --upgrade pip && \
    pip install --no-cache-dir sherpa-onnx fastapi uvicorn python-multipart

# ✅ DOWNLOAD MODEL FROM MODELSCOPE (100% Public & Fast)
# یہ لنک علی بابا کا اپنا ہے اور کبھی فیل نہیں ہوگا
RUN git clone https://www.modelscope.cn/k2-fsa/sherpa-onnx-tts-cosyvoice-300m-sft.git model_data

# Cleanup
RUN rm -rf model_data/.git

# ⚠️ Copy your voice file
COPY my_voice.wav .

COPY main.py .

CMD ["python", "main.py"]