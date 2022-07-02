FROM python:3-slim-buster

LABEL version="0.4"
LABEL description="Dockerfile for xonox backend"

WORKDIR /usr/src/app


ADD source /usr/src/app/
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
RUN  pip install .
EXPOSE 80
CMD ["python", "-m", "xonox", "--config-dir",  "/usr/src/app"]
