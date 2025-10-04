#!/bin/bash

echo "Starting HVAC Assistant Backend..."

# Wait for Qdrant to be available
echo "Waiting for Qdrant to be available..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s "${QDRANT_URL:-https://hvac-qdrant.azurewebsites.net}" > /dev/null; then
        echo "✅ Qdrant is available!"
        break
    fi
    echo "⏳ Waiting for Qdrant... (attempt $((attempt + 1))/$max_attempts)"
    sleep 10
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    echo "⚠️  Warning: Qdrant not available after ${max_attempts} attempts. Starting backend anyway..."
else
    # Run document ingestion
    echo "🔄 Running document ingestion..."
    cd /app
    python scripts/ingest.py
    echo "✅ Document ingestion completed!"
fi

# Start the FastAPI server
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000