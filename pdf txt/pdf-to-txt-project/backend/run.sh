#!/bin/bash

echo "========================================"
echo " PDF to TXT Converter - Flask Server"
echo "========================================"
echo ""

# 检查是否在backend目录中
if [ ! -f "app.py" ]; then
    echo "Error: Please run this script from the 'backend' directory!"
    echo "Current directory: $(pwd)"
    exit 1
fi

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 not found!"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# 检查依赖
echo "Checking Python dependencies..."
python3 -c "import flask, pdfplumber, flask_cors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies from requirements.txt..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies!"
        exit 1
    fi
fi

echo ""
echo "Starting Flask server on http://localhost:5000"
echo "Press CTRL+C to stop the server"
echo ""

# 运行Flask应用
python3 app.py

echo ""
echo "Server stopped."