FROM python:3.10.9-slim

# ENV POETRY_VERSION=1.3.2 \
#   POETRY_NO_INTERACTION=1 \
#   POETRY_VIRTUALENVS_CREATE=false

RUN useradd -u 8877 docker
USER docker

# RUN python -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# RUN pip install "poetry==$POETRY_VERSION"

# COPY pyproject.toml poetry.lock /mqtt/

# RUN poetry export --without-hashes --no-ansi -f requirements.txt -o requirements.txt
# RUN pip install -r requirements.txt

# Project initialization:
# RUN poetry config virtualenvs.create false \
#   && poetry install --no-interaction --no-ansi

# RUN pip install --no-cache-dir paho-mqtt==1.6.1 openai-whisper==20230117 numpy==1.24.1 pvporcupine==2.1.4 pvrecorder==1.1.1 scipy==1.10.0 torchaudio==0.13.1 pvcobra==1.2.0 python-dotenv==0.21.1 torch==1.13.1

WORKDIR /mqtt
COPY . /mqtt

# CMD ["python", "-u", "main.py"]