#!/usr/bin/env python3
"""
Start server with English output only to avoid encoding issues
"""
import os
import sys
import socket

def check_dependencies():
    """Check if all required packages are installed"""
    required = ['flask', 'pdfplumber', 'flask_cors']
    missing = []

    for package in required:
        try:
            if package == 'flask_cors':
                __import__('flask_cors')
            else:
                __import__(package)
        except ImportError:
            missing.append(package)

    return missing

def check_port(port):
    """Check if port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

def main():
    print("=" * 60)
    print("PDF to TXT Converter - Server Startup")
    print("=" * 60)

    # Check dependencies
    print("\n1. Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print(f"   ERROR: Missing packages: {', '.join(missing)}")
        print("   Please run: pip install -r requirements.txt")
        return 1

    print("   OK: All dependencies installed")

    # Check port
    port = 5000
    print(f"\n2. Checking port {port}...")
    if not check_port(port):
        print(f"   ERROR: Port {port} is already in use")
        print("   Please close the program using port 5000 or use:")
        print("   set FLASK_APP=app.py && flask run --port=5001")
        return 1

    print(f"   OK: Port {port} is available")

    # Check app.py
    print("\n3. Checking app.py...")
    if not os.path.exists("app.py"):
        print("   ERROR: app.py not found in current directory")
        return 1

    try:
        # Test import
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app import app
        print("   OK: app.py imports successfully")
    except Exception as e:
        print(f"   ERROR: Failed to import app.py: {e}")
        return 1

    # Start server
    print("\n4. Starting server...")
    print("-" * 40)
    print(f"Server URL: http://localhost:{port}")
    print(f"Health check: http://localhost:{port}/health")
    print(f"Frontend: http://localhost:{port}/")
    print("-" * 40)
    print("\nIMPORTANT: Keep this window open while using the converter")
    print("Press CTRL+C to stop the server")
    print("=" * 60)

    # Flush output
    sys.stdout.flush()

    # Start the server
    try:
        app.run(host='127.0.0.1', port=port, debug=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nServer failed to start: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    # Set encoding for Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    sys.exit(main())