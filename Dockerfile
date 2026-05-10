# syntax=docker/dockerfile:1.7
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --disable-pip-version-check "."
COPY .streamlit/ .streamlit/
COPY src/ src/
ENV PORT=8501 \
    PYTHONPATH=/app
EXPOSE 8501
CMD ["sh", "-c", "exec streamlit run src/ui/app.py --server.port=${PORT} --server.address=0.0.0.0"]
