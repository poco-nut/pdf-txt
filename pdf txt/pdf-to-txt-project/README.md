# PDF to TXT Converter Web Tool

A full-stack web application that converts PDF files to plain text (TXT) files. Built with Python Flask backend and modern HTML/CSS/JS frontend.

## Features

- Drag & drop PDF upload
- Real-time conversion progress indicator
- Automatic download of converted TXT file
- Clean, responsive UI with mobile support
- Secure temporary file cleanup
- Support for multi-page PDFs
- Page separation markers in output text

## Project Structure

```
pdf-to-txt-project/
├── backend/
│   ├── app.py              # Flask application with API endpoints
│   ├── parser.py           # PDF text extraction logic
│   ├── requirements.txt    # Python dependencies
│   ├── temp_uploads/       # Temporary PDF storage
│   └── temp_outputs/       # Temporary TXT storage
└── frontend/
    ├── index.html          # Main HTML interface
    ├── style.css           # Styling
    └── script.js           # Frontend logic
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation & Setup

1. **Clone or download the project**

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the Flask server (Easiest method):**
   - **Windows**: Double-click `START_SERVER.bat` in the main project folder
   - **Command line**: Open terminal in the `backend` folder and run:
     ```bash
     python start_simple.py
     ```
     or
     ```bash
     python app.py
     ```

   The server will start at `http://localhost:5000`

4. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage

1. Open the web application in your browser
2. Drag & drop a PDF file into the upload area, or click "Choose File"
3. Click "Convert to TXT" to start the conversion
4. Wait a few seconds for processing
5. The converted TXT file will automatically download
6. Use "Reset" to clear the current file and start over

## API Endpoints

- `POST /api/convert` - Convert PDF to TXT (expects `file` form field)
- `GET /health` - Health check endpoint
- `GET /` - Serve frontend interface

## Technical Details

### Backend
- **Framework**: Flask with CORS support
- **PDF Processing**: pdfplumber library for text extraction
- **File Handling**: UUID-based temporary file management with automatic cleanup
- **Error Handling**: Comprehensive error handling for invalid PDFs, missing files, etc.

### Frontend
- **Design**: Modern CSS with Flexbox/Grid
- **Interactivity**: Drag & drop, progress indicators, responsive feedback
- **API Integration**: Fetch API with proper error handling
- **Compatibility**: Works on all modern browsers

### Security Considerations
- File type validation (PDF only)
- File size limit (50MB)
- Temporary files are deleted after processing
- CORS configured for local development

## Limitations

- Scanned PDFs (image-based) may not produce accurate text
- Maximum file size: 50MB
- Complex PDF formatting may not be perfectly preserved
- For production use, consider adding:
  - Rate limiting
  - Authentication
  - Queue system for large files
  - Cloud storage integration

## Troubleshooting

### "Conversion failed" errors
- Ensure the PDF is not password-protected
- Check that the PDF contains extractable text (not scanned images)
- Verify file size is under 50MB

### Server won't start or stops immediately
If the server fails to start or stops immediately after starting:

1. **Run the diagnostic tool** to identify the exact problem:
   ```bash
   cd backend
   python start_diagnostic.py
   ```

2. **Common issues and solutions**:
   - **Missing dependencies**: Run `pip install -r requirements.txt`
   - **Port 5000 already in use**: Close other programs using port 5000, or use a different port
   - **Python encoding issues**: Use the provided batch files that handle encoding
   - **App code errors**: Check error messages in the console

3. **Use the fixed launcher**:
   - Double-click `start_fixed.bat` in the main project folder
   - This provides better error messages and handling

### 'python app.py' shows no output
If you run `python app.py` and see no output (the command seems to hang), try these solutions:

1. **Wait a few seconds** - Flask may take a moment to initialize
2. **Press Enter** - Sometimes output is buffered and needs a newline
3. **Use the provided startup scripts**:
   - Windows: Run `run.bat` in the backend directory
   - Linux/Mac: Run `./run.sh` in the backend directory
4. **Run with output unbuffered**:
   ```bash
   python -u app.py
   ```
5. **Check if server is already running**:
   ```bash
   # Windows
   netstat -an | findstr :5000
   # Linux/Mac
   netstat -an | grep :5000
   ```
6. **Alternative startup methods**:
   ```bash
   # Method 1: Set Python unbuffered environment variable
   set PYTHONUNBUFFERED=1 && python app.py
   
   # Method 2: Use flask run command
   set FLASK_APP=app.py && flask run --port=5000
   ```

If the server starts but you don't see output, it may still be running. Test by opening `http://localhost:5000/health` in your browser.

### Frontend not loading
- Ensure you're accessing `http://localhost:5000` not `file://`
- Check browser console for CORS errors (should be resolved with flask-cors)

## Development

To modify the application:

1. Backend changes: Edit `backend/app.py` or `backend/parser.py`
2. Frontend changes: Edit files in `frontend/` directory
3. After making changes, restart the Flask server

## License

This project is provided as-is for educational and personal use.

## Credits

Built with:
- [Flask](https://flask.palletsprojects.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Font Awesome](https://fontawesome.com/)
- [Google Fonts](https://fonts.google.com/)