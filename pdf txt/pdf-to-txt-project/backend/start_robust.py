#!/usr/bin/env python3
"""
Robust server startup with detailed error handling
"""
import os
import sys
import traceback
import time

def setup_output():
    """Setup console output for Windows"""
    if sys.platform == 'win32':
        try:
            # Try to set UTF-8 encoding
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass

    # Force immediate output
    sys.stdout.flush()
    sys.stderr.flush()

def print_header():
    """Print startup header"""
    print("\n" + "=" * 60)
    print("PDF to TXT Converter - Server Startup")
    print("=" * 60)

def print_footer():
    """Print shutdown footer"""
    print("\n" + "=" * 60)
    print("Server Stopped")
    print("=" * 60)

def check_dependencies():
    """Check if all required packages are installed"""
    required = [
        ('flask', 'Flask'),
        ('pdfplumber', 'PDFPlumber'),
        ('flask_cors', 'Flask-CORS')
    ]

    print("\nChecking dependencies...")
    missing = []
    for import_name, display_name in required:
        try:
            if import_name == 'flask_cors':
                __import__('flask_cors')
            else:
                __import__(import_name)
            print(f"  ✓ {display_name}")
        except ImportError:
            print(f"  ✗ {display_name} - MISSING")
            missing.append(import_name)

    if missing:
        print(f"\nERROR: Missing packages: {', '.join(missing)}")
        print("Please install with: pip install -r requirements.txt")
        return False

    return True

def import_app():
    """Try to import the Flask app with detailed error handling"""
    print("\nImporting application...")

    # Add current directory to path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    try:
        # First try to import parser separately to isolate errors
        try:
            import parser
            print("  ✓ parser.py imported")
        except Exception as e:
            print(f"  ⚠ parser.py import warning: {e}")

        # Import the main app
        from app import app
        print("  ✓ app.py imported")
        return app, None
    except Exception as e:
        print(f"  ✗ Failed to import app.py: {e}")
        return None, e

def start_server(app):
    """Start the Flask server"""
    print("\nStarting Flask server...")
    print("-" * 40)
    print(f"URL: http://localhost:5000")
    print(f"Health: http://localhost:5000/health")
    print("-" * 40)
    print("\nIMPORTANT:")
    print("1. Keep this window open")
    print("2. Open browser to http://localhost:5000")
    print("3. Press CTRL+C to stop")
    print("-" * 40)

    sys.stdout.flush()

    try:
        # Start server with NO reloader to avoid issues
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
        return True
    except KeyboardInterrupt:
        print("\nServer stopped by user (Ctrl+C)")
        return True
    except Exception as e:
        print(f"\nERROR: Server crashed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main function"""
    setup_output()
    print_header()

    try:
        # Step 1: Check dependencies
        if not check_dependencies():
            print_footer()
            return 1

        # Step 2: Import app
        app, import_error = import_app()
        if app is None:
            print("\nFULL ERROR DETAILS:")
            traceback.print_exc()
            print_footer()
            return 1

        # Step 3: Start server
        print("\nStarting server in 3 seconds...")
        for i in range(3, 0, -1):
            print(f"  {i}...")
            time.sleep(1)

        success = start_server(app)
        print_footer()
        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\nStartup interrupted by user")
        print_footer()
        return 1
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        traceback.print_exc()
        print_footer()
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        if exit_code != 0:
            print("\n" + "!" * 60)
            print("SERVER FAILED TO START")
            print("See error messages above for details.")
            print("!" * 60)
            print("\nPress Enter to exit...")
            try:
                input()
            except:
                pass
        sys.exit(exit_code)
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)