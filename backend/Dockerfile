# Using a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY backend/app/ ./app

# Copy documents and ingestion script (from build context root)
COPY docs/ ./docs/
COPY scripts/ ./scripts/

# Add startup script (from backend directory)
COPY backend/startup.sh ./startup.sh
# Fix line endings and make executable
RUN sed -i 's/\r$//' ./startup.sh && chmod +x ./startup.sh

# Expose port and use startup script
EXPOSE 8000
CMD ["./startup.sh"]