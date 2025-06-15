import os
import shutil
from flask import Flask, jsonify, send_file, request
import io

app = Flask(__name__)

# 模拟FTP文件存储
MOCK_FTP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock_ftp')

# 创建模拟FTP目录
os.makedirs(MOCK_FTP_DIR, exist_ok=True)

# FTP服务API
@app.route('/api/mock_ftp/upload', methods=['POST'])
def upload_file():
    """模拟FTP上传"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    version_dir = request.form.get('version_dir', 'default')
    filename = request.form.get('filename', file.filename)
    
    # 创建版本目录
    version_path = os.path.join(MOCK_FTP_DIR, version_dir)
    os.makedirs(version_path, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(version_path, filename)
    file.save(file_path)
    
    return jsonify({
        'filename': filename,
        'original_filename': file.filename,
        'file_path': f"file/{version_dir}/{filename}"
    })

@app.route('/api/mock_ftp/download/<path:file_path>', methods=['GET'])
def download_file(file_path):
    """模拟FTP下载"""
    # 路径转换
    file_path = file_path.replace('file/', '')
    full_path = os.path.join(MOCK_FTP_DIR, file_path)
    
    if not os.path.exists(full_path):
        return jsonify({'error': '文件不存在'}), 404
    
    return send_file(full_path, as_attachment=True)

@app.route('/api/mock_ftp/list/<path:directory>', methods=['GET'])
def list_files(directory):
    """模拟FTP列出目录文件"""
    directory = directory.replace('file/', '')
    full_path = os.path.join(MOCK_FTP_DIR, directory)
    
    if not os.path.exists(full_path):
        return jsonify({'error': '目录不存在'}), 404
    
    files = []
    for file in os.listdir(full_path):
        file_path = os.path.join(full_path, file)
        if os.path.isfile(file_path):
            files.append({
                'name': file,
                'size': os.path.getsize(file_path),
                'path': f"file/{directory}/{file}"
            })
    
    return jsonify(files)

@app.route('/api/mock_ftp/clean', methods=['POST'])
def clean_ftp():
    """清理模拟FTP存储"""
    if os.path.exists(MOCK_FTP_DIR):
        shutil.rmtree(MOCK_FTP_DIR)
        os.makedirs(MOCK_FTP_DIR, exist_ok=True)
    
    return jsonify({'status': 'success', 'message': 'FTP存储已清理'})

# 工具函数
@app.route('/api/mock_ftp/create_test_file', methods=['POST'])
def create_test_file():
    """创建测试文件，用于测试下载功能"""
    data = request.get_json()
    version_dir = data.get('version_dir', 'version_1')
    filename = data.get('filename', 'test_file.txt')
    content = data.get('content', 'This is a test file content.')
    
    # 创建版本目录
    version_path = os.path.join(MOCK_FTP_DIR, version_dir)
    os.makedirs(version_path, exist_ok=True)
    
    # 写入文件
    file_path = os.path.join(version_path, filename)
    with open(file_path, 'w') as f:
        f.write(content)
    
    return jsonify({
        'filename': filename,
        'file_path': f"file/{version_dir}/{filename}",
        'size': os.path.getsize(file_path)
    })

if __name__ == '__main__':
    print(f"模拟FTP服务器已启动在端口5001")
    print(f"FTP目录: {MOCK_FTP_DIR}")
    app.run(debug=True, port=5001) 