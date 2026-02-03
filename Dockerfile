FROM python:3.11-slim

WORKDIR /app

# =============================================================================
# BLACK SWARM - Network Isolated Self-Improving AI Runtime
# Supports both Claude Code CLI and Groq API backends
# =============================================================================

# Install system dependencies including Node.js for Claude Code
RUN apt-get update && apt-get install -y --no-install-recommends \
    iptables \
    dnsutils \
    iproute2 \
    procps \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (required for Claude Code CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Install Python dependencies
COPY requirements-groq.txt .
RUN pip install --no-cache-dir -r requirements-groq.txt

# Copy application code
COPY . .

# Fix line endings and make entrypoint executable
RUN sed -i 's/\r$//' docker-entrypoint.sh && chmod +x docker-entrypoint.sh

# Create directories
RUN mkdir -p /app/grind_logs /app/knowledge /app/experiments

# Environment
ENV PYTHONUNBUFFERED=1
ENV WORKSPACE=/app
# Default to auto engine selection
ENV INFERENCE_ENGINE=auto

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "grind_spawner_unified.py", "--delegate", "--budget", "1.00", "--once"]
