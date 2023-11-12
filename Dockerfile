FROM python:3-slim as builder
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
RUN pip install poetry
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN poetry install

FROM python:3-slim as base
LABEL version="1.0.0"
LABEL name="xonox"
LABEL author="TillW"
LABEL description="An alternative infrastructure-service for legacy NOXON(tm) devices."
LABEL url="https://github.com/x789/xonox/"
COPY --from=builder /app/xonox /app/xonox
COPY --from=builder /app/.venv/ /app/.venv
RUN mkdir /app/config
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 80
CMD ["python", "-m", "xonox", "--config-dir", "/app/config"]
