import os

from flask import Blueprint, request, jsonify, send_file
from app.services.version_service import VersionService
from loguru import logger

api_bp = Blueprint('api', __name__)


@api_bp.route('/versions', methods=['GET'])
def get_versions():
    """
    获取所有版本信息的API端点
    
    Returns:
        JSON响应，包含所有版本信息或错误信息
    """
    try:
        # 从服务层获取所有版本
        versions = VersionService.get_all_versions()
        # 返回成功响应，包含所有版本的数据
        return jsonify({
            'status': 'success',
            'data': [version.to_dict() for version in versions]
        })
    except Exception as e:
        # 记录错误日志
        logger.error(f"Error getting versions: {str(e)}")
        # 返回错误响应
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500  # HTTP 500 服务器内部错误


@api_bp.route('/versions/<int:version_id>', methods=['GET'])
def get_version(version_id):
    """
    获取指定ID版本信息的API端点
    
    Args:
        version_id: 版本ID
        
    Returns:
        JSON响应，包含指定版本信息或错误信息
    """
    try:
        # 从服务层获取指定ID的版本
        version = VersionService.get_version_by_id(version_id)
        # 如果版本不存在，返回404错误
        if not version:
            return jsonify({
                'status': 'error',
                'message': 'Version not found'
            }), 404  # HTTP 404 资源不存在

        # 返回成功响应，包含版本数据
        return jsonify({
            'status': 'success',
            'data': version.to_dict()
        })
    except Exception as e:
        # 记录错误日志
        logger.error(f"Error getting version: {str(e)}")
        # 返回错误响应
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500  # HTTP 500 服务器内部错误


@api_bp.route('/versions', methods=['POST'])
def create_version():
    """
    创建新版本的API端点
    
    请求中需包含版本信息和文件（如有）
    
    Returns:
        JSON响应，包含创建的版本信息或错误信息
    """
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400  # HTTP 400 请求错误

        # 获取上传的文件
        file = request.files['file']
        # 获取表单中的版本数据
        version_data = request.form.to_dict()

        # 验证版本号是否提供
        if not version_data.get('version'):
            return jsonify({
                'status': 'error',
                'message': 'Version number is required'
            }), 400  # HTTP 400 请求错误

        # 调用服务层创建版本
        version = VersionService.create_version(version_data, file)
        # 返回成功响应，包含创建的版本数据
        return jsonify({
            'status': 'success',
            'data': version.to_dict()
        }), 201  # HTTP 201 资源已创建
    except Exception as e:
        # 记录错误日志
        logger.error(f"Error creating version: {str(e)}")
        # 返回错误响应
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500  # HTTP 500 服务器内部错误


@api_bp.route('/versions/<int:version_id>', methods=['PUT'])
def update_version(version_id):
    """
    更新指定ID版本的API端点
    
    Args:
        version_id: 要更新的版本ID
        
    Returns:
        JSON响应，包含更新后的版本信息或错误信息
    """
    try:
        # 获取表单中的版本数据
        version_data = request.form.to_dict()
        # 获取上传的文件（如果有）
        file = request.files.get('file')

        # 调用服务层更新版本
        version = VersionService.update_version(version_id, version_data, file)
        # 如果版本不存在，返回404错误
        if not version:
            return jsonify({
                'status': 'error',
                'message': 'Version not found'
            }), 404  # HTTP 404 资源不存在

        # 返回成功响应，包含更新后的版本数据
        return jsonify({
            'status': 'success',
            'data': version.to_dict()
        })
    except Exception as e:
        # 记录错误日志
        logger.error(f"Error updating version: {str(e)}")
        # 返回错误响应
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500  # HTTP 500 服务器内部错误


@api_bp.route('/versions/<int:version_id>', methods=['DELETE'])
def delete_version(version_id):
    """
    删除指定ID版本的API端点
    
    Args:
        version_id: 要删除的版本ID
        
    Returns:
        JSON响应，包含删除操作状态信息
    """
    try:
        # 调用服务层删除版本
        success = VersionService.delete_version(version_id)
        # 如果版本不存在，返回404错误
        if not success:
            return jsonify({
                'status': 'error',
                'message': 'Version not found'
            }), 404  # HTTP 404 资源不存在

        # 返回成功响应
        return jsonify({
            'status': 'success',
            'message': 'Version deleted successfully'
        })
    except Exception as e:
        # 记录错误日志
        logger.error(f"Error deleting version: {str(e)}")
        # 返回错误响应
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500  # HTTP 500 服务器内部错误


@api_bp.route('/versions/<int:version_id>/download', methods=['GET'])
def download_version(version_id):
    """
    下载指定ID版本关联文件的API端点
    
    Args:
        version_id: 版本ID
        
    Returns:
        文件下载响应或错误信息
    """
    try:
        # 从服务层获取指定ID的版本
        version = VersionService.get_version_by_id(version_id)
        # 如果版本不存在或没有关联文件，返回404错误
        if not version or not version.file_path:
            return jsonify({
                'status': 'error',
                'message': 'Version or file not found'
            }), 404  # HTTP 404 资源不存在

        # 返回文件下载响应
        return send_file(
            version.file_path,  # 文件路径
            as_attachment=True,  # 作为附件下载
            download_name=os.path.basename(version.file_path)  # 设置下载文件名
        )
    except Exception as e:
        # 记录错误日志
        logger.error(f"Error downloading version: {str(e)}")
        # 返回错误响应
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500  # HTTP 500 服务器内部错误