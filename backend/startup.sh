#!/bin/bash

echo "Starting HVAC Assistant Backend..."

# Wait for Qdrant to be available
QDRANT_URL="${QDRANT_URL:-https://hvac-qdrant.azurewebsites.net}"
echo "Waiting for Qdrant to be available at: $QDRANT_URL"
max_attempts=6  # (1 minute total)
attempt=0

while [ $attempt -lt $max_attempts ]; do
    # Use Python for health check with better error handling
    check_result=$(python -c "
import requests
import sys
try:
    print(f'Checking: $QDRANT_URL')
    response = requests.get('$QDRANT_URL', timeout=10)
    print(f'Response: {response.status_code}')
    if response.status_code == 200:
        print('SUCCESS')
        sys.exit(0)
    else:
        print(f'HTTP {response.status_code}')
        sys.exit(1)
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "✅ Qdrant is available!"
        echo "$check_result"
        break
    else
        echo "⏳ Waiting for Qdrant... (attempt $((attempt + 1))/$max_attempts)"
        echo "Debug: $check_result"
        sleep 10
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -eq $max_attempts ]; then
    echo "⚠️  Warning: Qdrant not available after ${max_attempts} attempts."
    echo "🚀 Starting backend anyway - Qdrant connection will be checked at runtime."
else
    # Check if collection already has data (smart ingestion)
    echo "🔍 Checking if HVAC documents are already ingested..."
    cd /app
    
    # Check collection status using simple HTTP request
    collection_count=$(python -c "
import requests
import os

url = os.getenv('QDRANT_URL', 'https://hvac-qdrant.azurewebsites.net')

try:
    response = requests.get(f'{url}/collections/hvac_docs', timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        points_count = data.get('result', {}).get('points_count', 0)
        print(points_count)
    else:
        print('0')
except Exception as e:
    print('0')
")
    
    if [ "$collection_count" -gt "0" ]; then
        echo "✅ Found $collection_count vectors already in collection. Skipping ingestion."
    else
        echo "� Collection is empty. Running document ingestion..."
        python scripts/ingest.py
        echo "✅ Document ingestion completed!"
    fi
fi

# Start the FastAPI server
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000