#!/usr/bin/env python3
"""
Minimal test server to debug startup issues.
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

print("Project paths added")

# Try importing modules one by one
try:
    from fastapi import FastAPI
    print("FastAPI imported")
except Exception as e:
    print(f"Failed FastAPI: {e}")

try:
    import data
    print("data module imported")
except Exception as e:
    print(f"Failed data: {e}")

try:
    import main
    print("main module imported")
except Exception as e:
    print(f"Failed main: {e}")

try:
    from main import app
    print("app imported from main")
except Exception as e:
    print(f"Failed app import: {e}")

# Create a simple FastAPI app if the full one fails
app = FastAPI(title="Test App")

@app.get("/")
async def root():
    return {"message": "Test server is running"}

@app.get("/test")
async def test():
    return {"status": "OK"}

print("Simple test app created")

if __name__ == "__main__":
    import uvicorn
    print("Starting uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8011)