#!/usr/bin/env python3
"""
Daemon server that runs independently
"""
import sys
import os
import signal
import time
import atexit
from pathlib import Path

# Fork to background
pid = os.fork()
if pid > 0:
    # Parent exits
    print(f"Server started with PID {pid}")
    sys.exit(0)

# Child continues
os.setsid()

# Second fork to ensure no controlling terminal
pid = os.fork()
if pid > 0:
    sys.exit(0)

# Redirect standard file descriptors
sys.stdout.flush()
sys.stderr.flush()
with open('/dev/null', 'r') as f:
    os.dup2(f.fileno(), sys.stdin.fileno())
with open('/tmp/daemon_server.log', 'a') as f:
    os.dup2(f.fileno(), sys.stdout.fileno())
    os.dup2(f.fileno(), sys.stderr.fileno())

# Ignore all signals
for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT, signal.SIGUSR1, signal.SIGUSR2]:
    try:
        signal.signal(sig, signal.SIG_IGN)
    except:
        pass

# Write PID file
with open('/tmp/hey_big_proppa_server.pid', 'w') as f:
    f.write(str(os.getpid()))

# Now run the server
sys.path.insert(0, str(Path("/home/sub-acct/Hey-Big-Proppa")))
sys.path.insert(0, str(Path("/home/sub-acct/Hey-Big-Proppa/backend")))

from backend.main import app
import uvicorn

print(f"Daemon server starting on port 8086, PID {os.getpid()}")
uvicorn.run(app, host='0.0.0.0', port=8086, log_level='info', timeout_keep_alive=300, timeout_graceful_shutdown=0)