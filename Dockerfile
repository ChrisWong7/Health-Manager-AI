# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/backend/

# Copy frontend code (backend/main.py expects it at ../frontend relative to itself)
COPY frontend/ /app/frontend/

# Expose port 8000
EXPOSE 8000

# Set PYTHONPATH
ENV PYTHONPATH=/app/backend

# Command to run the application
WORKDIR /app/backend
CMD ["python", "main.py"]
