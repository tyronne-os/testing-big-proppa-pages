#!/usr/bin/env python3
"""
Local server startup script for Hey-Big-Proppa
"""
import os
import sys
from pathlib import Path

# Set up paths
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Import the main app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

# Create a new app
app = FastAPI(title="HEY BIG PROPPA!")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files if they exist
dist_dir = project_root / "frontend" / "dist"
if dist_dir.exists() and (dist_dir / "index.html").exists():
    print(f"Serving frontend from {dist_dir}")
    app.mount("/static", StaticFiles(directory=str(dist_dir)), name="static")
    
    @app.get("/")
    async def root():
        return FileResponse(str(dist_dir / "index.html"))
        
    @app.get("/{path:path}")
    async def catch_all(path: str):
        file_path = dist_dir / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(dist_dir / "index.html"))
else:
    @app.get("/")
    async def root():
        return HTMLResponse("<h1>HEY BIG PROPPA!</h1><p>Local server running</p>")

# Basic API endpoint
@app.get("/api")
async def api():
    return {"app": "HEY BIG PROPPA!", "status": "running"}

# Player data endpoint
@app.get("/api/chart/player_props")
async def player_props(player_id: str, market: str):
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

# Parlay endpoints
@app.get("/api/chart/parlays")
async def api_parlays(slip: str = "hot_dogs"):
    try:
        import parlays
        fn = parlays.SLIPS.get(slip)
        if not fn:
            from fastapi import HTTPException
            raise HTTPException(400, f"unknown slip '{slip}', expected one of {list(parlays.SLIPS)}")
        result = fn()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/chart/parlays/all")
async def api_parlays_all():
    try:
        import parlays
        slips = {}
        for slip_id, fn in parlays.SLIPS.items():
            try:
                slips[slip_id] = fn()
            except Exception as e:
                slips[slip_id] = {"error": str(e)}
        return slips
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("Starting Hey-Big-Proppa local server")
    print("Access the site at: http://localhost:8000")
    print("API endpoint at: http://localhost:8000/api")
    print("Parlay data at: http://localhost:8000/api/chart/parlays/all")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")