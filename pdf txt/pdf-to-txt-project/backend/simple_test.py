#!/usr/bin/env python3
"""
简易测试脚本，验证Flask是否能启动
"""
import socket
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! Flask is working!"

@app.route('/test')
def test():
    return jsonify({"status": "ok", "message": "Server is running"})

def check_port(port):
    """检查端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

if __name__ == '__main__':
    port = 5000

    print("=" * 50)
    print("Flask简易测试服务器")
    print("=" * 50)

    # 检查端口
    if not check_port(port):
        print(f"[ERROR] 端口 {port} 已被占用！")
        print("请关闭占用5000端口的程序，或使用其他端口：")
        print("  python simple_test.py --port 5001")
        exit(1)

    print(f"[OK] 端口 {port} 可用")
    print("正在启动Flask服务器...")
    print(f"访问地址：http://localhost:{port}")
    print(f"测试页面：http://localhost:{port}/test")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)

    try:
        # 确保输出立即显示
        import sys
        sys.stdout.flush()

        # 启动服务器
        app.run(host='127.0.0.1', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败：{e}")
        import traceback
        traceback.print_exc()