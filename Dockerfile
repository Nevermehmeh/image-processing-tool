# Build stage
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libvips-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY . .

# Runtime stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libvips-tools \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser && \
    mkdir -p /app/static/uploads /app/static/outputs /app/static/temp /app/logs && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Set environment variables
ENV FLASK_APP=wsgi:app \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Switch to non-root user
USER appuser

# Run the application
CMD ["gunicorn", "--worker-class=gevent", "--worker-connections=1000", "--workers=4", "--timeout", "120", "--bind", "0.0.0.0:5000", "wsgi:app"]
