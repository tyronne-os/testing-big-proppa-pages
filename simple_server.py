#!/usr/bin/env python3
"""
Simple server script with error collection
"""
import socket
import sys
import signal
import os
from pathlib import Path

# Check if port is available
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.bind(("localhost", port))
            return True
        except (socket.error, socket.timeout):
            return False

if not is_port_available(8010):
    print("Port 8010 is not available. Trying to clean it up...")
    os.system("lsof -ti:8010 | xargs kill -9 2>/dev/null || echo 'No process to kill'")
    
# Print each step of the startup process
print("=== Starting Hey-Big-Proppa server ===")
print("Working directory:", os.getcwd())
print("Python executable:", sys.executable)

# Add path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

print("Importing FastAPI...")
try:
    from fastapi import FastAPI
except Exception as e:
    print(f"FastAPI import failed: {e}")
    sys.exit(1)

print("Importing main...")
try:
    from main import app
except Exception as e:
    print(f"Main import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Starting uvicorn server...")
try:
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010, reload=False, log_level="info")
except KeyboardInterrupt:
    print("\nServer stopped by user")
except Exception as e:
    print(f"Server failed to start: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)