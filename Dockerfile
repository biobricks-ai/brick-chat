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
COPY instructions/ ./instructions/
COPY chainlit.md ./

RUN uv sync --frozen --no-dev

ENV GOOGLE_GENAI_USE_VERTEXAI=True

EXPOSE 6525

CMD ["uv", "run", "chainlit", "run", "src/app.py", "--port", "6525"]