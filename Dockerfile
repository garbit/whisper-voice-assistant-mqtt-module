FROM python:3.11.1-slim

RUN pip install --no-cache-dir paho-mqtt==1.6.1

RUN useradd -u 8877 docker
USER docker

WORKDIR /mqtt
COPY . /mqtt

CMD ["python", "-u", "main.py"]