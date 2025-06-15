from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__)

# 添加处理CORS预检请求的路由
@api_bp.route('/', methods=['OPTIONS'])
@api_bp.route('/<path:path>', methods=['OPTIONS'])
def handle_options_request(path=None):
    return jsonify({"status": "ok"}), 200

from app.api.routes import api_bp

# 导入所有资源，确保路由正确注册
from app.api.resources import auth
from app.api.resources import user
from app.api.resources import version
from app.api.resources import product
from app.api.resources import file
from app.api.resources import role
from app.api.resources import user_product_permission
from app.api.resources import operation_log
