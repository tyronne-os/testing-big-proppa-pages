#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse("<h1>HEY BIG PROPPA!</h1><p>Server is running on port 8000</p>")

@app.get("/api")
async def api():
    return {"status": "running", "message": "Quick test server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)