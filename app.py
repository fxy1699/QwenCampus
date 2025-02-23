from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'images' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('images')
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            # 生成安全的文件名
            filename = secure_filename(file.filename)
            # 添加唯一标识符防止文件名冲突
            unique_filename = f"{str(uuid.uuid4())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            try:
                file.save(file_path)
                # 这里返回相对路径，实际使用时需要配置正确的域名
                file_url = f"/uploads/{unique_filename}"
                uploaded_files.append(file_url)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    return jsonify({
        'message': 'Files uploaded successfully',
        'urls': uploaded_files
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # 这里处理与 AI 模型的交互
    # 示例响应
    response = {
        'role': 'assistant',
        'content': '这是来自后端的 AI 响应'
    }
    return jsonify(response)

@app.route('/model-info', methods=['GET'])
def model_info():
    # 这里获取模型信息
    return jsonify({
        'model_name': 'qwen2.5:14b',
        'status': 'ready'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)