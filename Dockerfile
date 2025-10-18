# Multi-stage build to reduce image size
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libhdf5-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000
ENV PATH="/root/.local/bin:$PATH"

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy only necessary application files
COPY app.py .
COPY requirements.txt .
COPY templates/ templates/
COPY static/ static/
COPY lstm_btc_daily_model.h5 .
COPY scaler_minmax.joblib .

# Create necessary directories
RUN mkdir -p static templates

# Set proper permissions
RUN chmod -R 755 /app

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
