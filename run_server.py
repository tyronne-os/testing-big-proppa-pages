#!/usr/bin/env python3
import sys
import os
import signal
from pathlib import Path

# Ignore SIGTERM to prevent being killed
signal.signal(signal.SIGTERM, signal.SIG_IGN)

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / 'backend'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn

project_root = Path.cwd()
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

dist_dir = project_root / 'frontend' / 'dist'
if dist_dir.exists():
    app.mount('/static', StaticFiles(directory=str(dist_dir)), name='static')
    
    @app.get('/')
    async def root():
        return FileResponse(str(dist_dir / 'index.html'))

@app.get('/api')
async def api():
    return {'app': 'HEY BIG PROPPA!', 'status': 'running'}

print('Starting server on http://0.0.0.0:8000...')
print('Press Ctrl+C to stop')
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')