from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid
from utils.lsky import Lsky
import time
from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL, CozeAPIError

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

# Coze配置
# 初始化 Lsky 和 Coze
lsky = Lsky()
COZE_API_TOKEN = 'pat_lU9WPsqEBNhJYPtl6j9QEnoi3E8D44x6BUkhP4BStHHvSE7o13U85JeyHKPk5KOL'
WORKFLOW_ID = '7474835190277128231'
coze = Coze(auth=TokenAuth(token=COZE_API_TOKEN), base_url=COZE_CN_BASE_URL)

def call_workflow_with_retry(image_url, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            workflow = coze.workflows.runs.create(
                workflow_id=WORKFLOW_ID,
                parameters={
                    "input": image_url
                }
            )
            return workflow.data
        except CozeAPIError as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                continue
            raise
    return None

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'GET':
        files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            file_url = f"/uploads/{filename}"
            files.append(file_url)
        return jsonify({'files': files})
    
    # 1. 检查文件是否存在
    if 'images' not in request.files:
        return jsonify({
            'status': 'error',
            'step': 'file_check',
            'message': '未找到上传的文件'
        }), 400
    
    files = request.files.getlist('images')
    results = []
    
    for file in files:
        result = {
            'original_filename': file.filename,
            'status': 'processing'
        }
        
        # 2. 验证文件类型
        if not (file and allowed_file(file.filename)):
            result.update({
                'status': 'error',
                'step': 'file_validation',
                'message': '不支持的文件类型'
            })
            results.append(result)
            continue
        
        try:
            # 3. 保存到本地
            filename = secure_filename(file.filename)
            unique_filename = f"{str(uuid.uuid4())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            result['local_url'] = f"/uploads/{unique_filename}"
            
            # 4. 上传到图床
            try:
                lsky_result = lsky.lsky_upload_images(file_path, filename)
                result['lsky_url'] = lsky_result['url']
                
                # 5. 调用图像识别
                try:
                    analysis = call_workflow_with_retry(lsky_result['url'])
                    result.update({
                        'status': 'success',
                        'analysis': analysis
                    })
                except Exception as e:
                    result.update({
                        'status': 'error',
                        'step': 'image_analysis',
                        'message': f'图像识别失败: {str(e)}'
                    })
            except Exception as e:
                result.update({
                    'status': 'error',
                    'step': 'lsky_upload',
                    'message': f'图床上传失败: {str(e)}'
                })
        except Exception as e:
            result.update({
                'status': 'error',
                'step': 'local_save',
                'message': f'本地保存失败: {str(e)}'
            })
        
        results.append(result)
    
    # 统计处理结果
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = len(results) - success_count
    
    return jsonify({
        'message': f'处理完成: {success_count} 成功, {error_count} 失败',
        'results': results
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

# 添加一个新路由来提供图片访问
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)