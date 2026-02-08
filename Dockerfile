FROM python:3.11-slim

WORKDIR /app

# Install Node.js for frontend build
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt gunicorn

# Copy all source files
COPY . .

# Build frontend
WORKDIR /app/frontend
RUN npm ci && npm run build

# Back to root
WORKDIR /app

# Populate database if it doesn't exist
RUN python populate_db.py

# Expose port
EXPOSE 5000

# Run with gunicorn - use shell form so $PORT is expanded
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 backend.app:app
