# =============================================================================
# Multi-Stage Dockerfile for Customer Journey Analysis Tool
# Optimized for production deployment on Hetzner CPX21 (4GB RAM, 2 vCPU)
# =============================================================================

# =============================================================================
# Stage 1: Builder
# Install dependencies and build wheel packages
# =============================================================================
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (creates .venv)
RUN uv sync --frozen --no-dev

# Copy application source
COPY src/ ./src/

# =============================================================================
# Stage 2: Runtime
# Minimal runtime image with only necessary dependencies
# =============================================================================
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy virtual environment from builder
COPY --from=builder /build/.venv /app/.venv

# Copy application source
COPY --from=builder /build/src /app/src

# Copy additional configuration files
COPY pyproject.toml /app/

# Create required directories
RUN mkdir -p /app/logs /data/obsidian_vault /data/recordings && \
    chown -R appuser:appuser /app /data

# Switch to non-root user
USER appuser

# Expose FastAPI port
EXPOSE 8030

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8030/health || exit 1

# Start application with Uvicorn
# Workers calculated based on CPU cores (2 * cores + 1 = 5 workers)
CMD ["uvicorn", "src.main:app", \
    "--host", "0.0.0.0", \
    "--port", "8030", \
    "--workers", "4", \
    "--loop", "uvloop", \
    "--log-level", "info", \
    "--access-log", \
    "--proxy-headers", \
    "--forwarded-allow-ips", "*"]
