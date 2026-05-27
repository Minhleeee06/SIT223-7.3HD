FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (enables Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ ./src/

# Set environment variables
ENV PORT=3000
ENV PYTHONUNBUFFERED=1

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:3000/health')"

CMD ["python", "src/app.py"]