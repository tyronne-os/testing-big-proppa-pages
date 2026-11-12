#!/usr/bin/env python3
"""
Server that runs with an explicit keep-alive loop
"""
import sys
import os
import signal
import asyncio
import threading
from pathlib import Path

# Fork to background
pid = os.fork()
if pid > 0:
    print(f"Server started with PID {pid}")
    sys.exit(0)

os.setsid()

pid = os.fork()
if pid > 0:
    sys.exit(0)

sys.stdout.flush()
sys.stderr.flush()
with open('/dev/null', 'r') as f:
    os.dup2(f.fileno(), sys.stdin.fileno())
with open('/tmp/daemon_server_v3.log', 'a') as f:
    os.dup2(f.fileno(), sys.stdout.fileno())
    os.dup2(f.fileno(), sys.stderr.fileno())

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT, signal.SIGUSR1, signal.SIGUSR2]:
    try:
        signal.signal(sig, signal.SIG_IGN)
    except:
        pass

with open('/tmp/hey_big_proppa_server.pid', 'w') as f:
    f.write(str(os.getpid()))

sys.path.insert(0, str(Path("/home/sub-acct/Hey-Big-Proppa")))
sys.path.insert(0, str(Path("/home/sub-acct/Hey-Big-Proppa/backend")))

import uvicorn
from backend.main import app

async def run_server():
    config = uvicorn.Config(app, host='0.0.0.0', port=8086, log_level='info', timeout_keep_alive=300)
    server = uvicorn.Server(config)
    print(f"Server starting on port 8086, PID {os.getpid()}")
    
    # Run serve in background
    serve_task = asyncio.create_task(server.serve())
    
    # Keep the event loop alive
    try:
        while not server.should_exit:
            await asyncio.sleep(10)
            print(f"Server keep-alive: {os.getpid()}, should_exit={server.should_exit}")
    except asyncio.CancelledError:
        pass
    finally:
        await serve_task

if __name__ == "__main__":
    asyncio.run(run_server())