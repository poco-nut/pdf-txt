# -*- coding: utf-8 -*-
import os
import uuid
import shutil
from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from parser import convert_pdf_to_txt

app = Flask(__name__)
CORS(app)  # 允许跨域请求
print("Flask app initialized successfully", flush=True)

# 配置上传和输出文件夹
UPLOAD_FOLDER = 'temp_uploads'
OUTPUT_FOLDER = 'temp_outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/api/convert', methods=['POST'])
def convert_pdf():
    """
    接收一个PDF文件，将其转换为TXT文件并返回。
    """
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # 如果用户没有选择文件
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 确保文件是PDF
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400

    # 生成唯一ID，避免文件名冲突
    unique_id = str(uuid.uuid4())
    pdf_filename = f"{unique_id}.pdf"
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

    # 保存上传的PDF
    file.save(pdf_path)

    try:
        # 调用转换函数
        txt_filename = f"{unique_id}.txt"
        txt_path = os.path.join(OUTPUT_FOLDER, txt_filename)

        success = convert_pdf_to_txt(pdf_path, txt_path)

        if not success:
            return jsonify({'error': 'Failed to convert PDF'}), 500

        # 返回TXT文件给前端
        return send_file(
            txt_path,
            as_attachment=True,
            download_name=f"{os.path.splitext(file.filename)[0]}.txt",
            mimetype='text/plain'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # 清理临时文件（无论成功与否）
        cleanup_files(pdf_path, txt_path if 'txt_path' in locals() else None)

def cleanup_files(pdf_path, txt_path):
    """
    删除临时PDF和TXT文件。
    """
    try:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
    except Exception:
        pass

    try:
        if txt_path and os.path.exists(txt_path):
            os.remove(txt_path)
    except Exception:
        pass

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({'status': 'healthy'})

# 静态文件服务 - 提供前端文件
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), '../frontend')

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)

if __name__ == '__main__':
    print("Starting Flask server on port 5000...", flush=True)
    print("Press CTRL+C to stop the server", flush=True)
    app.run(debug=True, port=5000)