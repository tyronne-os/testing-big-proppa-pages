#!/bin/bash
# Test script to see if our issues stem from connection issues

# Start server in background
echo "Starting server on 8010..."
cd /home/sub-acct/Hey-Big-Proppa/backend
source ../.venv/bin/activate

# Run server with output captured
python -m uvicorn main:app --host 0.0.0.0 --port 8010 --log-level debug 2>&1 | sed -u 's/^/[SERVER] /' &
SERVER_PID=$!

# Give server time to start
echo "Waiting for server to start..."
sleep 3

# Check if server is responding
echo "Testing server response..."
curl -s http://localhost:8010 && echo "Server responded!" || echo "Server not responding"

# Show some server logs
echo "Server logs:"
sleep 2
kill $SERVER_PID 2>/dev/null || true