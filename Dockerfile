# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Update system packages and install required packages
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy pyproject.toml, uv.lock, and README.md for dependency installation
COPY pyproject.toml uv.lock README.md ./

# Install dependencies with uv
RUN uv sync --frozen --no-dev --no-native-tls

# Copy application files
COPY . .

# Set Python path to src directory
ENV PYTHONPATH="/app/src"
ENV LOG_DIR="/app/logs"

# Create fonts and logs directories
RUN mkdir -p fonts logs

# Default command - parameters are passed directly to python main.py
ENTRYPOINT ["uv", "run", "python", "-m", "font_analyzer.main"]
