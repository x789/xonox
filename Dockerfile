FROM python:3-slim

LABEL version="1.0.0"
LABEL name="xonox"
LABEL description="xonox - an alternative service for legacy NOXON(tm) devices"
LABEL url="https://github.com/x789/xonox/"

WORKDIR /app
ADD source/src /app

RUN mkdir /app/config
RUN pip install --upgrade pip
RUN pip install flask
EXPOSE 80
CMD ["python", "-m", "xonox", "--config-dir", "/app/config"]
