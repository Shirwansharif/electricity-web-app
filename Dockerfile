FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn python-multipart aiofiles websockets

# Copy application
COPY app_simple.py app.py
COPY templates/ templates/
COPY static/ static/

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
