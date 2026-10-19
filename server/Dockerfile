FROM python:3.13-slim
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
USER app
ENV DATA_DIR=/data \
    HOST=0.0.0.0 \
    PORT=8080 \
    PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "-m", "cognio_server"]
