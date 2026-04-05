#!/usr/bin/env python3
"""
Diagnostic script to identify why Flask server fails to start
"""
import os
import sys
import traceback
import socket

def print_step(step_num, message):
    """Print a diagnostic step with clear formatting"""
    print(f"\n[Step {step_num}] {message}")
    print("-" * 60)

def check_python():
    """Step 1: Check Python version and environment"""
    print_step(1, "Checking Python environment")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")

    # Check if we're in the backend directory
    if not os.path.exists("app.py"):
        print("ERROR: app.py not found in current directory!")
        print("Please run this script from the 'backend' directory.")
        return False
    return True

def check_imports():
    """Step 2: Check if required packages are installed"""
    print_step(2, "Checking required packages")

    required_packages = [
        ('flask', 'Flask'),
        ('pdfplumber', 'pdfplumber'),
        ('flask_cors', 'flask_cors')
    ]

    all_ok = True
    for import_name, display_name in required_packages:
        try:
            if import_name == 'flask_cors':
                __import__('flask_cors')
            else:
                __import__(import_name)
            print(f"✓ {display_name}: OK")
        except ImportError as e:
            print(f"✗ {display_name}: MISSING - {e}")
            all_ok = False

    return all_ok

def check_port():
    """Step 3: Check if port 5000 is available"""
    print_step(3, "Checking port 5000")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()

        if result == 0:
            print("✗ Port 5000 is already in use")
            print("  Another program is using port 5000.")
            print("  Solution: Close that program or use a different port.")
            return False
        else:
            print("✓ Port 5000 is available")
            return True
    except Exception as e:
        print(f"? Could not check port: {e}")
        return True  # Assume it's OK if we can't check

def check_app_import():
    """Step 4: Try to import the Flask app"""
    print_step(4, "Importing Flask app")

    try:
        # Add current directory to Python path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        print("Attempting to import app.py...")

        # First try to import parser separately
        try:
            import parser
            print("✓ parser.py: Import successful")
        except Exception as e:
            print(f"✗ parser.py: Import failed - {e}")
            print("  This might cause app.py import to fail.")

        # Now try to import app
        from app import app
        print("✓ app.py: Import successful")
        print(f"  Flask app name: {app.name}")
        return True
    except Exception as e:
        print(f"✗ app.py: Import failed")
        print(f"  Error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def test_flask_start():
    """Step 5: Try to start the Flask server briefly"""
    print_step(5, "Testing Flask server startup")

    try:
        from app import app

        # We'll run in a separate thread to test briefly
        import threading
        import time

        server_started = threading.Event()
        server_error = None

        def run_server():
            try:
                print("Starting Flask server (test mode)...")
                # Run with use_reloader=False to avoid double startup
                app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
            except Exception as e:
                nonlocal server_error
                server_error = e
            finally:
                server_started.set()

        # Start server in background thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait a few seconds for server to start or fail
        print("Waiting for server to start (max 10 seconds)...")
        for i in range(10):
            time.sleep(1)
            print(f"  {i+1}s...", end='\r')

            # Check if thread is still alive
            if not server_thread.is_alive():
                print(f"\n✗ Server thread stopped unexpectedly")
                if server_error:
                    print(f"  Error: {server_error}")
                return False

            # Try to connect to the server
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', 5000))
                sock.close()
                if result == 0:
                    print(f"\n✓ Server started successfully on port 5000!")
                    print("  Note: Server will continue running in background.")
                    print("  Press Ctrl+C in the terminal to stop it.")
                    return True
            except:
                pass

        print(f"\n✗ Server did not start within 10 seconds")
        print("  The server thread might be hanging or stuck.")
        return False

    except Exception as e:
        print(f"✗ Failed to test server startup: {e}")
        traceback.print_exc()
        return False

def main():
    """Main diagnostic function"""
    print("=" * 70)
    print("PDF to TXT Converter - Server Diagnostic Tool")
    print("=" * 70)

    # Force UTF-8 output for Windows
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

    # Run all checks
    steps = [
        ("Python Environment", check_python),
        ("Package Dependencies", check_imports),
        ("Port Availability", check_port),
        ("App Import", check_app_import),
        ("Server Startup", test_flask_start),
    ]

    results = []
    for name, check_func in steps:
        print(f"\n{'='*70}")
        print(f"CHECKING: {name}")
        print('='*70)
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"Error during check: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("SUCCESS: All checks passed!")
        print("Your server should start normally.")
        print("\nTo start the server, run:")
        print("  python start_simple.py")
    else:
        print("ISSUES FOUND: Some checks failed.")
        print("Please fix the issues above before starting the server.")

    print("=" * 70)

    # Write results to file for reference
    try:
        with open("diagnostic_results.txt", "w", encoding="utf-8") as f:
            f.write("Diagnostic Results:\n")
            for name, passed in results:
                f.write(f"{'PASS' if passed else 'FAIL'}: {name}\n")
        print("\nResults saved to: diagnostic_results.txt")
    except Exception as e:
        print(f"\nCould not save results to file: {e}")

    return 0 if all_passed else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error in diagnostic: {e}")
        traceback.print_exc()
        sys.exit(1)