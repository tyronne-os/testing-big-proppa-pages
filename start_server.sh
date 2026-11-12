#!/bin/bash
# Start script for Hey-Big-Proppa
cd "$(dirname "$0")"

echo "Starting Hey-Big-Proppa server..."

# Activate virtual environment
source .venv/bin/activate

# Set PYTHONPATH to include backend directory
export PYTHONPATH="${PWD}:${PWD}/backend:$PYTHONPATH"

# Start the server with explicit port binding
python -c "
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / 'backend'))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Check if frontend is built
dist_dir = Path.cwd() / 'frontend' / 'dist'
if (dist_dir / 'index.html').exists():
    print(f'Serving frontend from {dist_dir}')
    app.mount('/static', StaticFiles(directory=str(dist_dir)), name='static')
    
    @app.get('/')
    async def root():
        return FileResponse(str(dist_dir / 'index.html'))
        
    @app.get('/{path:path}')
    async def catch_all(path: str):
        file_path = dist_dir / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(dist_dir / 'index.html'))
else:
    @app.get('/')
    async def root():
        return HTMLResponse('<h1>HEY BIG PROPPA!</h1><p>Server running</p>')

# Simple API endpoint
@app.get('/api')
async def api():
    return {'app': 'HEY BIG PROPPA!', 'status': 'running'}

print('Starting uvicorn server on http://0.0.0.0:8000')
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
"