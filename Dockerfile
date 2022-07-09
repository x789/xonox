FROM python:3-slim-buster

LABEL version="0.0.7"
LABEL description="Dockerfile for xonox backend"

WORKDIR /app
ADD source/src /app

RUN mkdir /app/config
RUN pip install --upgrade pip
RUN pip install flask
EXPOSE 80
CMD ["python", "-m", "xonox", "--config-dir", "/app/config"]
