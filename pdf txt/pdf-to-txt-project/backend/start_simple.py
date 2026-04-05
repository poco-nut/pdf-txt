#!/usr/bin/env python3
"""
Simplest possible server startup - no debug, no reloader, English only
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("=" * 50)
    print("PDF to TXT Converter Server")
    print("=" * 50)
    print("Server starting on: http://localhost:5000")
    print("Frontend: http://localhost:5000")
    print("Health check: http://localhost:5000/health")
    print("")
    print("IMPORTANT:")
    print("1. Keep this window open")
    print("2. Open browser to http://localhost:5000")
    print("3. Press CTRL+C to stop")
    print("=" * 50)

    # Force output flush
    sys.stdout.flush()

    # Start server - NO debug, NO reloader
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\nPress Enter to exit...")
    input()
    sys.exit(1)