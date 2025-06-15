from flask import Blueprint
from app.api.resources.auth import LoginResource
from app.api.resources.user import UserResource, UserListResource
from app.api.resources.version import VersionResource, VersionListResource, VersionHistoryResource
from app.api.resources.product import ProductResource, ProductListResource
from app.api.resources.file import FileUploadResource, FileDownloadResource, FileListResource, FileDeleteResource
from app.api.resources.role import RoleResource, RoleListResource
from app.api.resources.user_product_permission import UserProductPermissionResource, UserProductPermissionListResource
from app.api.resources.operation_log import (
    OperationLogResource, OperationLogListResource, 
    ObjectOperationLogResource, UserOperationLogResource,
    VersionStatusHistoryResource
)

api_bp = Blueprint('api', __name__)

# 认证相关路由
api_bp.add_url_rule('/auth/login', view_func=LoginResource.as_view('auth_login'))

# 用户相关路由
api_bp.add_url_rule('/users', view_func=UserListResource.as_view('user_list'))
api_bp.add_url_rule('/users/<int:user_id>', view_func=UserResource.as_view('user_detail'))

# 角色相关路由
api_bp.add_url_rule('/roles', view_func=RoleListResource.as_view('role_list'))
api_bp.add_url_rule('/roles/<int:role_id>', view_func=RoleResource.as_view('role_detail'))

# 产品相关路由
api_bp.add_url_rule('/products', view_func=ProductListResource.as_view('product_list'))
api_bp.add_url_rule('/products/<int:product_id>', view_func=ProductResource.as_view('product_detail'))

# 版本相关路由
api_bp.add_url_rule('/versions', view_func=VersionListResource.as_view('version_list'))
api_bp.add_url_rule('/versions/<int:version_id>', view_func=VersionResource.as_view('version_detail'))
api_bp.add_url_rule('/products/<int:product_id>/versions', view_func=VersionHistoryResource.as_view('product_versions'))
api_bp.add_url_rule('/versions/<int:version_id>/status-history', view_func=VersionStatusHistoryResource.as_view('version_status_history'))

# 文件相关路由
api_bp.add_url_rule('/files', view_func=FileListResource.as_view('file_list'))
api_bp.add_url_rule('/files/upload', view_func=FileUploadResource.as_view('file_upload'))
api_bp.add_url_rule('/files/download/<int:file_id>', view_func=FileDownloadResource.as_view('file_download'))
api_bp.add_url_rule('/files/<int:file_id>', view_func=FileDeleteResource.as_view('file_delete'), methods=['DELETE'])

# 用户产品权限相关路由
api_bp.add_url_rule('/user-product-permissions', view_func=UserProductPermissionListResource.as_view('permission_list'))
api_bp.add_url_rule('/user-product-permissions/<int:perm_id>', view_func=UserProductPermissionResource.as_view('permission_detail'))

# 操作日志相关路由
api_bp.add_url_rule('/operation-logs', view_func=OperationLogListResource.as_view('operation_log_list'))
api_bp.add_url_rule('/operation-logs/<int:log_id>', view_func=OperationLogResource.as_view('operation_log_detail'))
api_bp.add_url_rule('/objects/<string:object_type>/<string:object_id>/logs', 
                   view_func=ObjectOperationLogResource.as_view('object_logs'))
api_bp.add_url_rule('/users/<int:user_id>/logs', view_func=UserOperationLogResource.as_view('user_logs'))