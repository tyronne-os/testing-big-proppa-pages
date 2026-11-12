#!/usr/bin/env python3
"""
Test script to see if the main app can be initialized
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

print("=== Testing module imports ===")

try:
    print("Importing data module...")
    import data
    print("Data module imported successfully")
    
    print("Testing player_dimension function...")
    player_dim = data.player_dimension()
    print(f"Player dimension loaded: {len(player_dim)} entries")
    
    print("Checking test player (00-0036212):")
    test_player = player_dim.get("00-0036212")
    if test_player:
        print(f"  Name: {test_player['name']}")
        print(f"  Team: {test_player['team']}")
        print(f"  Position: {test_player['position']}")
    else:
        print("  Player not found")
    
    print("Data module tests completed successfully")
except Exception as e:
    import traceback
    print(f"Error in data module: {e}")
    traceback.print_exc()

try:
    print("\nImporting main module...")
    from fastapi import FastAPI
    app = FastAPI(title="Test App")
    
    import main
    print("Main module imported successfully")
    
    print("\nAll tests completed successfully!")
except Exception as e:
    import traceback
    print(f"Error in main module: {e}")
    traceback.print_exc()