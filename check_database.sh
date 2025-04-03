#!/bin/bash

# Source DATABASE_URL from the .env file
if [ -f ./.env ]; then
  echo "Loading environment variables from .env file..."
  export $(grep -v '^#' .env | grep DATABASE_URL | xargs)
fi

# Check if DATABASE_URL is defined
if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DATABASE_URL is not defined in environment variables or .env file"
  
  # Try to get it from Replit environment
  echo "Checking Replit system environment..."
  REPLIT_DB_URL=$(curl -s $REPLIT_DB_URL/.env/DATABASE_URL)
  
  if [ ! -z "$REPLIT_DB_URL" ]; then
    export DATABASE_URL="$REPLIT_DB_URL"
    echo "Found DATABASE_URL in Replit environment"
  else
    exit 1
  fi
fi

echo "Checking database tables..."

# SQL query to get table names
QUERY="SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"

# Execute the query using psql
psql "$DATABASE_URL" -c "$QUERY"

echo "Database check completed"