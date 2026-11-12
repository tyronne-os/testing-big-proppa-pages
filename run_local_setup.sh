#!/bin/bash
# A script to run the Hey-Big-Proppa backend and check that it's working

set -e

echo "=== Setting up Hey-Big-Proppa local environment ==="

# Create a new terminal window with the app running
cd "$(dirname "$0")"
echo "Setting up from $(pwd)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install a minimal set of dependencies
echo "Installing minimal dependencies..."
pip install fastapi uvicorn pandas

# Start the server
echo "Starting server on port 8010..."
echo "Open your browser to: http://localhost:8010"
echo "Press Ctrl+C to stop the server"

cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8010 --log-level info