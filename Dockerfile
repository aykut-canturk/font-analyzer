# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy all required files before installing dependencies
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Sync dependencies (installs them into system, uv creates virtualenv internally)
RUN uv sync

# Set environment variables
ENV PYTHONPATH="/app/src"
ENV PYTHONUNBUFFERED=1
ENV LOG_DIR="/app/logs"

# Create required directories
RUN mkdir -p /app/fonts /app/logs

# Default command
ENTRYPOINT ["uv", "run", "python", "-m", "font_analyzer.main"]
