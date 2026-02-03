# Dockerfile for Black Swarm - Network-Isolated AI Execution Environment
#
# This container locks down all network access except:
# - Groq API (api.groq.com)
# - Localhost (127.0.0.1)
#
# Build: docker build -t black-swarm .
# Run:   docker run --env-file .env -v $(pwd)/workspace:/app/workspace black-swarm

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    iptables \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -s /bin/bash swarm && \
    mkdir -p /app/workspace /app/grind_logs && \
    chown -R swarm:swarm /app

# Copy requirements first for caching
COPY requirements-groq.txt .
RUN pip install --no-cache-dir -r requirements-groq.txt

# Copy application code
COPY --chown=swarm:swarm . /app/

# Network isolation script (run as root before dropping privileges)
COPY --chown=root:root network_lockdown.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/network_lockdown.sh

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV WORKSPACE=/app/workspace

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from groq_client import get_groq_engine; print('OK')" || exit 1

# Default command
ENTRYPOINT ["/usr/local/bin/network_lockdown.sh"]
CMD ["python", "grind_spawner_groq.py", "--delegate", "--model", "llama-3.1-8b-instant", "--budget", "0.20"]
