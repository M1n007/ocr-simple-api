FROM ubuntu:18.04

RUN apt-get update -y

RUN apt-get install -y \
    libsm6 \
    libxext6 \
    tesseract-ocr \
    python3-pip \
    python3-dev \
    build-essential

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["server.py"]

