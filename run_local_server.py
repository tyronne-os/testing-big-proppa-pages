#!/usr/bin/env python3
"""
Local development server for Hey-Big-Proppa.
This script starts the FastAPI backend on port 8000 and serves the frontend.
"""
import os
import sys
import subprocess
import threading
import time
from pathlib import Path

# Add the backend directory to the path
backend_path = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_path))

# Import required modules
import uvicorn
from main import app

def start_backend():
    """Start the FastAPI backend server."""
    print("Starting backend server on http://localhost:8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

def start_frontend():
    """Start the frontend development server."""
    frontend_path = Path(__file__).resolve().parent / "frontend"
    os.chdir(frontend_path)
    
    print("Installing frontend dependencies...")
    subprocess.run(["export", "PATH=\"$HOME/Downloads/node-v26.13.1-linux-x64/bin:$PATH\""], shell=True)
    subprocess.run(["npm", "ci"], check=True)
    
    print("Building frontend...")
    subprocess.run(["npm", "run", "build"], check=True)
    
    print("Starting frontend dev server on http://localhost:3000...")
    subprocess.run(["npm", "run", "dev"])

def main():
    """Start both backend and frontend servers."""
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(2)
    
    # Start frontend (this will block)
    start_frontend()

if __name__ == "__main__":
    main()