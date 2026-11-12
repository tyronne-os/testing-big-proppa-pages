#!/usr/bin/env python3
"""
Daemon server that runs independently using asyncio
"""
import sys
import os
import signal
import asyncio
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
with open('/tmp/daemon_server_v2.log', 'a') as f:
    os.dup2(f.fileno(), sys.stdout.fileno())
    os.dup2(f.fileno(), sys.stderr.fileno())

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT, signal.SIGUSR1, signal.SIGUSR2]:
    try:
        signal.signal(sig, signal.SIG_IGN)
    except:
        pass

with open('/tmp/hey_big_proppa_server.pid', 'w') as f:
    f.write(str(os.getpid()))

# Set up paths
sys.path.insert(0, str(Path("/home/sub-acct/Hey-Big-Proppa")))
sys.path.insert(0, str(Path("/home/sub-acct/Hey-Big-Proppa/backend")))

# Import and run
import uvicorn
from backend.main import app

async def run_server():
    config = uvicorn.Config(app, host='0.0.0.0', port=8086, log_level='info', timeout_keep_alive=300)
    server = uvicorn.Server(config)
    print(f"Daemon server starting on port 8086, PID {os.getpid()}")
    await server.serve()

if __name__ == "__main__":
    asyncio.run(run_server())