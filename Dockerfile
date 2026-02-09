FROM python:3.11-slim

WORKDIR /app

# =============================================================================
# BLACK SWARM - Network Isolated Self-Improving AI Runtime
# Groq-only inference backend
# =============================================================================

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    iptables \
    dnsutils \
    iproute2 \
    procps \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-groq.txt .
RUN pip install --no-cache-dir -r requirements-groq.txt

# Copy application code
COPY . .

# Fix line endings and make entrypoint executable
RUN sed -i 's/\r$//' docker-entrypoint.sh && chmod +x docker-entrypoint.sh

# Create directories
RUN mkdir -p /app/grind_logs /app/knowledge /app/experiments /app/data

# Create non-root user for security (UID 1000 matches most host users)
RUN useradd -m -u 1000 swarm && \
    chown -R swarm:swarm /app/grind_logs /app/experiments /app/data && \
    chmod +x docker-entrypoint.sh

# Environment
ENV PYTHONUNBUFFERED=1
ENV WORKSPACE=/app
# Default to Groq engine selection
ENV INFERENCE_ENGINE=groq

# Switch to non-root user (critical security hardening)
USER swarm

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "grind_spawner_unified.py", "--delegate", "--budget", "1.00", "--once"]
