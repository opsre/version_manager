import json
from datetime import datetime
from app.extensions import db
from app.models.operation_log import OperationLog

class OperationLogService:
    @staticmethod
    def create_log(operation_type, object_type, object_name, object_id, operator_id, details=None):
        """创建操作日志"""
        # 如果details是字典，转换为JSON字符串
        if isinstance(details, dict):
            details = json.dumps(details, ensure_ascii=False)
            
        log = OperationLog(
            operation_type=operation_type,
            object_type=object_type,
            object_name=object_name,
            object_id=str(object_id),
            operator_id=operator_id,
            details=details
        )
        
        db.session.add(log)
        db.session.commit()
        return log
    
    @staticmethod
    def get_log_by_id(log_id):
        """根据ID获取日志"""
        return OperationLog.query.get(log_id)
    
    @staticmethod
    def get_logs(page=1, per_page=20, operation_type=None, object_type=None, 
                 object_id=None, operator_id=None, start_time=None, end_time=None):
        """获取日志列表，支持多种条件过滤和分页"""
        query = OperationLog.query
        
        # 应用过滤条件
        if operation_type:
            query = query.filter(OperationLog.operation_type == operation_type)
        if object_type:
            query = query.filter(OperationLog.object_type == object_type)
        if object_id:
            query = query.filter(OperationLog.object_id == str(object_id))
        if operator_id:
            query = query.filter(OperationLog.operator_id == operator_id)
        
        # 时间范围过滤
        if start_time:
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(OperationLog.operation_time >= start_time)
        if end_time:
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(OperationLog.operation_time <= end_time)
        
        # 按时间倒序排序
        query = query.order_by(OperationLog.operation_time.desc())
        
        # 分页
        return query.paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_logs_by_object(object_type, object_id, page=1, per_page=20):
        """获取特定对象的所有操作日志"""
        query = OperationLog.query.filter_by(
            object_type=object_type, 
            object_id=str(object_id)
        ).order_by(OperationLog.operation_time.desc())
        
        return query.paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_logs_by_operator(operator_id, page=1, per_page=20):
        """获取特定操作人的所有操作日志"""
        query = OperationLog.query.filter_by(
            operator_id=operator_id
        ).order_by(OperationLog.operation_time.desc())
        
        return query.paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_version_status_history(version_id):
        """获取版本状态变更历史
        
        包括：
        1. 创建版本
        2. 状态变更（如从"开发中"到"测试中"，"测试中"到"已发布"等）
        3. 锁定/解锁版本
        """
        # 获取该版本的所有相关日志
        logs = OperationLog.query.filter(
            OperationLog.object_type == '版本',
            OperationLog.object_id == str(version_id),
            # 只获取与状态相关的操作类型
            OperationLog.operation_type.in_(['创建', '状态变更', '发布', '废弃', '锁定', '解锁'])
        ).order_by(OperationLog.operation_time.asc()).all()
        
        return logs 