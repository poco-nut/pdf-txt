#!/usr/bin/env python3
"""
Test Flask server with 0.0.0.0 binding
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! Server with 0.0.0.0 is working!"

@app.route('/health')
def health():
    return {"status": "ok", "binding": "0.0.0.0"}

if __name__ == '__main__':
    print("=" * 50)
    print("TEST Flask Server (0.0.0.0)")
    print("=" * 50)
    print("Starting on http://0.0.0.0:5002")
    print("Access via: http://localhost:5002/health")
    print("=" * 50)

    # Use 0.0.0.0 to bind to all interfaces
    app.run(host='0.0.0.0', port=5002, debug=False, use_reloader=False)