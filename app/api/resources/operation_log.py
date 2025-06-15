from flask import request
from flask.views import MethodView
from app.services.operation_log_service import OperationLogService
from app.services.version_service import VersionService

class OperationLogListResource(MethodView):
    def get(self):
        """获取操作日志列表，支持多种条件过滤"""
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        operation_type = request.args.get('operation_type')
        object_type = request.args.get('object_type')
        object_id = request.args.get('object_id')
        operator_id = request.args.get('operator_id', type=int)
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        # 查询日志
        pagination = OperationLogService.get_logs(
            page=page,
            per_page=per_page,
            operation_type=operation_type,
            object_type=object_type,
            object_id=object_id,
            operator_id=operator_id,
            start_time=start_time,
            end_time=end_time
        )
        
        logs = pagination.items
        
        return {
            'success': True,
            'data': {
                'logs': [log.to_dict() for log in logs],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page
            }
        }

class OperationLogResource(MethodView):
    def get(self, log_id):
        """获取单条操作日志详情"""
        log = OperationLogService.get_log_by_id(log_id)
        
        if not log:
            return {'success': False, 'message': '日志不存在'}, 404
        
        return {
            'success': True,
            'data': log.to_dict()
        }

class ObjectOperationLogResource(MethodView):
    def get(self, object_type, object_id):
        """获取特定对象的操作日志"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = OperationLogService.get_logs_by_object(
            object_type=object_type,
            object_id=object_id,
            page=page,
            per_page=per_page
        )
        
        logs = pagination.items
        
        return {
            'success': True,
            'data': {
                'logs': [log.to_dict() for log in logs],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page
            }
        }

class UserOperationLogResource(MethodView):
    def get(self, user_id):
        """获取特定用户的操作日志"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = OperationLogService.get_logs_by_operator(
            operator_id=user_id,
            page=page,
            per_page=per_page
        )
        
        logs = pagination.items
        
        return {
            'success': True,
            'data': {
                'logs': [log.to_dict() for log in logs],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page
            }
        }

class VersionStatusHistoryResource(MethodView):
    def get(self, version_id):
        """获取版本状态变更历史"""
        # 检查版本是否存在
        version = VersionService.get_version_by_id(version_id)
        if not version:
            return {'success': False, 'message': '版本不存在'}, 404
            
        # 获取该版本的所有状态变更日志
        # 包括创建、状态变更、锁定/解锁操作
        logs = OperationLogService.get_version_status_history(version_id)
        
        # 转换为前端需要的格式
        history_items = []
        for log in logs:
            item = {
                'operator_name': log.operator.name if log.operator else '未知用户',
                'operator_id': log.operator_id,
                'operation_type': log.operation_type,
                'operation_time': log.operation_time.strftime('%Y-%m-%d %H:%M:%S'),
                'details': log.details
            }
            
            # 添加到结果列表
            history_items.append(item)
            
        return {
            'success': True,
            'data': {
                'version': version.to_dict(),
                'history': history_items
            }
        } 