#!/usr/bin/env python3
"""
Simple test Flask server to check if Flask works at all
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! Test server is working!"

@app.route('/health')
def health():
    return {"status": "ok", "test": True}

if __name__ == '__main__':
    print("=" * 50)
    print("TEST Flask Server")
    print("=" * 50)
    print("Starting on http://127.0.0.1:5001")
    print("Test with: http://localhost:5001/health")
    print("=" * 50)

    # Use port 5001 to avoid conflict with main app
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)