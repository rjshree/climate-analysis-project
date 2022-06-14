FROM python:3.8-slim-buster
LABEL maintainer="r.tutgirl@gmail.com"
WORKDIR /app
COPY requirements.txt /app

RUN apt-get update && apt-get install -y build-essential \
    && pip install -r requirements.txt --no-cache-dir \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && rm -rf /var/tmp/*
COPY . /app
ENV "PYTHONUNBUFFERED" 1
ENV "PYTHONPATH" "/app"
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "--bind","0.0.0.0:5000", "--chdir", "climate_api","api:app"]