# Use Python 3.8 slim image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY Pipfile ./

# Install Python dependencies directly from Pipfile
RUN pip install --no-cache-dir \
    flask \
    flask-admin \
    flask-bootstrap \
    flask-cache \
    flask-flatpages \
    flask-gravatar \
    flask-login \
    flask-mail \
    flask-pymongo \
    flask-restless \
    flask-sqlalchemy \
    flask-themes \
    flask-uploads \
    flask-wtf \
    flask-cors \
    requests \
    werkzeug

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "run.py"]

