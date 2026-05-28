FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY App.py .

# Set environment variables
ENV PORT=3000
ENV PYTHONUNBUFFERED=1

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:3000/health')"

CMD ["python", "App.py"]
