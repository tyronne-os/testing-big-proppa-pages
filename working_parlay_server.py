#!/usr/bin/env python3
"""
Working parlay server with basic endpoints
"""
import sys
from pathlib import Path

# Set up paths
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Simple FastAPI app with just the parlay endpoints
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json

# Create app
app = FastAPI(title="HEY BIG PROPPA! API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if we can serve the frontend
def get_frontend_path():
    dist_dir = project_root / "frontend" / "dist"
    if (dist_dir / "index.html").exists():
        return dist_dir
    return None

# API endpoints
@app.get("/")
async def root():
    frontend_path = get_frontend_path()
    if frontend_path:
        return FileResponse(str(frontend_path / "index.html"))
    return HTMLResponse("<h1>HEY BIG PROPPA!</h1><p>Parlay server running</p>")

@app.get("/api")
async def api_info():
    return {"app": "HEY BIG PROPPA!", "status": "running", "version": "parlay-test"}

# Add parlay endpoints
@app.get("/api/chart/parlays")
async def api_parlays(slip: str = "hot_dogs"):
    try:
        import parlays
        print(f"Fetching parlay for slip: {slip}")
        fn = parlays.SLIPS.get(slip)
        if not fn:
            raise HTTPException(400, f"unknown slip '{slip}', expected one of {list(parlays.SLIPS)}")
        result = fn()
        print(f"Parlay result type: {type(result)}")
        return result
    except Exception as e:
        print(f"Error in api_parlays: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/api/chart/parlays/all")
async def api_parlays_all():
    try:
        import parlays
        print("Fetching all parlays")
        slips = {}
        for slip_id, fn in parlays.SLIPS.items():
            print(f"Processing slip: {slip_id}")
            try:
                slips[slip_id] = fn()
            except Exception as e:
                print(f"Error processing {slip_id}: {e}")
                slips[slip_id] = {"error": str(e)}
        return slips
    except Exception as e:
        print(f"Error in api_parlays_all: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

# Player slug endpoints
_SLUGS_FILE = project_root / "lake" / "gold" / "espn" / "player_slugs.json"

def load_slugs():
    try:
        return json.loads(_SLUGS_FILE.read_text())
    except:
        return {}

@app.get("/api/slug/list")
async def slug_list():
    slugs = load_slugs()
    return {"count": len(slugs), "slugs": slugs}

@app.get("/api/slug/resolve/{slug}")
async def slug_resolve(slug: str):
    slugs = load_slugs()
    entry = slugs.get(slug)
    if not entry:
        raise HTTPException(404, f"unknown slug {slug}")
    return entry

if __name__ == "__main__":
    import uvicorn
    print("Starting working parlay server on http://localhost:8017")
    print("Frontend at: http://localhost:8017")
    print("Parlay endpoint at: http://localhost:8017/api/chart/parlays/all")
    uvicorn.run(app, host="0.0.0.0", port=8017, log_level="info")