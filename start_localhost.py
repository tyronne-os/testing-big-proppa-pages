#!/usr/bin/env python3
"""
Simple localhost server runner for Hey-Big-Proppa.
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Starting Hey-Big-Proppa localhost environment...")
    
    # Check if frontend is built
    frontend_dist = Path(__file__).resolve().parent / "frontend" / "dist"
    if not frontend_dist.exists():
        print("📦 Building frontend...")
        subprocess.run([
            "npm",
            "run",
            "build"
        ], cwd=Path(__file__).resolve().parent / "frontend")
    
    # Start the backend server
    backend_dir = Path(__file__).resolve().parent / "backend"
    print(f"🌟 Starting backend server from {backend_dir}...")
    print("📍 Open your browser to: http://localhost:8000")
    print("📋 API docs at: http://localhost:8000/docs")
    print("\n\nPress Ctrl+C to stop the server\n")
    
    # Use venv uvicorn
    project_root = Path(__file__).resolve().parent
    venv_python = project_root / ".venv" / "bin" / "python"
    
    os.chdir(backend_dir)
    subprocess.run([
        str(venv_python),
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload"
    ])

if __name__ == "__main__":
    main()