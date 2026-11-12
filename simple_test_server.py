#!/usr/bin/env python3
"""
Very simple test server to check if parlays module works
"""
import sys
from pathlib import Path

# Set up paths
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

print("Testing parlays module import...")
try:
    import parlays
    print("parlays module imported")
    print("SLIPS:", list(parlays.SLIPS.keys()))
    
    # Try to call one of the functions
    hot_dogs_fn = parlays.SLIPS.get("hot_dogs")
    if hot_dogs_fn:
        result = hot_dogs_fn()
        print(f"hot_dogs result type: {type(result)}")
    else:
        print("hot_dogs function not found")
        
except Exception as e:
    print(f"Error importing parlays: {e}")
    import traceback
    traceback.print_exc()