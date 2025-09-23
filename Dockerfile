FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential 

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY .chainlit/ ./.chainlit/
COPY instructions/ ./instructions/
COPY chainlit.md main.py ./

RUN uv sync --frozen --no-dev

ENV GOOGLE_GENAI_USE_VERTEXAI=True

EXPOSE 6525

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:6525/health || exit 1

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6525"]