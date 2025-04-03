#!/bin/bash
set -e

echo "Starting FastAPI backend on port 8000..."
cd backend

# Set environment variables (showing only that they're set, not the values)
echo "Database configuration:"
echo "- DATABASE_URL exists: $(if [ -n "$DATABASE_URL" ]; then echo "yes"; else echo "no"; fi)"
echo "- PGDATABASE exists: $(if [ -n "$PGDATABASE" ]; then echo "yes"; else echo "no"; fi)"
echo "- PGUSER exists: $(if [ -n "$PGUSER" ]; then echo "yes"; else echo "no"; fi)"
echo "- PGHOST exists: $(if [ -n "$PGHOST" ]; then echo "yes"; else echo "no"; fi)"
echo "- PGPORT exists: $(if [ -n "$PGPORT" ]; then echo "yes"; else echo "no"; fi)"

# Run FastAPI directly (no timeout)
python3 -m uvicorn direct_main:app --host 0.0.0.0 --port 8000
