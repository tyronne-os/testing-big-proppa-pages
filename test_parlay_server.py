#!/usr/bin/env python3
"""
Test parlay server with just the parlay endpoints
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
from fastapi.staticfiles import StaticFiles
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

# Static files
dist_dir = project_root / "frontend" / "dist"
if dist_dir.exists():
    app.mount("/static", StaticFiles(directory=str(dist_dir)), name="static")

# API endpoints
@app.get("/")
async def root():
    if dist_dir.exists():
        return FileResponse(str(dist_dir / "index.html"))
    return {"message": "HEY BIG PROPPA!"}

@app.get("/api")
async def api_info():
    return {"app": "HEY BIG PROPPA!", "status": "running"}

# Add parlay endpoints
@app.get("/api/chart/parlays")
async def api_parlays(slip: str = "hot_dogs"):
    try:
        import parlays
        fn = parlays.SLIPS.get(slip)
        if not fn:
            raise HTTPException(400, f"unknown slip '{slip}', expected one of {list(parlays.SLIPS)}")
        return fn()
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/chart/parlays/all")
async def api_parlays_all():
    try:
        import parlays
        slips = {slip_id: fn() for slip_id, fn in parlays.SLIPS.items()}
        return slips
    except Exception as e:
        return {"error": str(e)}

# Test with player dimension data
@app.get("/api/chart/player_props")
async def player_props_test(player_id: str, market: str):
    try:
        import data
        players = data.player_dimension()
        player = players.get(player_id)
        if player:
            return {
                "player_name": player.get("name", "Unknown"),
                "position": player.get("position", ""),
                "team": player.get("team", ""),
                "player_id": player_id
            }
        else:
            return {"error": "Player not found"}
    except Exception as e:
        return {"error": str(e)}

# Player slug endpoints
from pathlib import Path as _Path
_SLUGS_FILE = _Path(__file__).resolve().parent / "lake" / "gold" / "espn" / "player_slugs.json"

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
    print("Starting parlay test server on http://localhost:8016")
    print("Frontend should be at: http://localhost:8016")
    print("Parlay endpoints: http://localhost:8016/api/chart/parlays/all")
    uvicorn.run(app, host="0.0.0.0", port=8016)