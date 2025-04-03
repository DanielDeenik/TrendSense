#!/bin/bash
set -e

echo "Testing Sustainability Intelligence Platform Integration..."

# Create logs directory
mkdir -p logs

# Check database connectivity
echo "Step 1: Checking database connectivity..."
if [ -n "$DATABASE_URL" ]; then
  echo "Database URL is set, environment looks good"
else
  echo "Warning: DATABASE_URL not set, database connectivity might fail"
fi

# Test FastAPI backend health
echo "Step 2: Testing FastAPI backend health..."
FASTAPI_URL=${BACKEND_URL:-"http://localhost:8000"}
echo "Using FastAPI URL: $FASTAPI_URL"

# Retry logic for backend health check
MAX_RETRIES=5
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  HEALTH_RESPONSE=$(curl -s -m 5 "$FASTAPI_URL/health" || echo "")
  if [ -n "$HEALTH_RESPONSE" ]; then
    echo "Backend health response: $HEALTH_RESPONSE"
    break
  fi

  RETRY_COUNT=$((RETRY_COUNT+1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "❌ FastAPI backend is not responding after $MAX_RETRIES attempts"
    echo "Check if the backend is running with: ps aux | grep uvicorn"
  else
    echo "Waiting for FastAPI backend to respond (attempt $RETRY_COUNT/$MAX_RETRIES)..."
    sleep 3
  fi
done

# Check if the health response includes "database":"connected"
if [[ "$HEALTH_RESPONSE" == *"\"database\":\"connected\""* ]]; then
  echo "✅ FastAPI backend is connected to PostgreSQL database"
else
  echo "❌ FastAPI backend cannot connect to PostgreSQL database"
fi

# Test FastAPI metrics endpoint
echo "Step 3: Testing FastAPI metrics endpoint..."
METRICS_RESPONSE=$(curl -s -m 5 "$FASTAPI_URL/api/metrics" || echo "[]")
METRICS_COUNT=$(echo "$METRICS_RESPONSE" | grep -o "\"id\"" | wc -l)
echo "Backend returned $METRICS_COUNT metrics"

if [ "$METRICS_COUNT" -gt 0 ]; then
  echo "✅ FastAPI backend successfully returned metrics from PostgreSQL"
else
  echo "❌ FastAPI backend didn't return any metrics"
fi

# Test Flask frontend
echo "Step 4: Testing Flask frontend..."
FLASK_URL="http://localhost:5000"
echo "Using Flask URL: $FLASK_URL"

# Retry logic for frontend check
MAX_RETRIES=5
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  DASHBOARD_RESPONSE=$(curl -s -m 5 "$FLASK_URL/dashboard" || echo "")
  if [ -n "$DASHBOARD_RESPONSE" ]; then
    break
  fi

  RETRY_COUNT=$((RETRY_COUNT+1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "❌ Flask frontend is not responding after $MAX_RETRIES attempts"
    echo "Check if the frontend is running with: ps aux | grep flask"
  else
    echo "Waiting for Flask frontend to respond (attempt $RETRY_COUNT/$MAX_RETRIES)..."
    sleep 3
  fi
done

if [[ "$DASHBOARD_RESPONSE" == *"Sustainability Intelligence Dashboard"* ]]; then
  echo "✅ Flask frontend dashboard page is accessible"
else
  echo "❌ Flask frontend dashboard page is not accessible"
fi

# Test the debug endpoint
DEBUG_RESPONSE=$(curl -s -m 5 "$FLASK_URL/debug" || echo "{}")
echo "Frontend debug response: $DEBUG_RESPONSE"

# Print summary
echo ""
echo "Integration Test Summary:"
echo "========================="
echo "1. PostgreSQL Database: $(if [[ "$HEALTH_RESPONSE" == *"\"database\":\"connected\""* ]]; then echo "✅ Connected"; else echo "❌ Not connected"; fi)"
echo "2. FastAPI Backend: $(if [ "$METRICS_COUNT" -gt 0 ]; then echo "✅ Working ($METRICS_COUNT metrics)"; else echo "❌ Not working"; fi)"
echo "3. Flask Frontend: $(if [[ "$DASHBOARD_RESPONSE" == *"Sustainability Intelligence Dashboard"* ]]; then echo "✅ Working"; else echo "❌ Not working"; fi)"
echo ""

echo "Done testing integration."