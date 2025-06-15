from datetime import datetime
from app.extensions import db
from app.models.version import Version

class VersionService:
    @staticmethod
    def create_version(product_id, version_number, description, release_notes, author_id, status='draft', lock_status=False):
        """创建新版本"""
        version = Version(
            product_id=product_id,
            version_number=version_number,
            description=description,
            release_notes=release_notes,
            author_id=author_id,
            status=status,
            lock_status=lock_status
        )
        
        db.session.add(version)
        db.session.commit()
        return version
    
    @staticmethod
    def get_version_by_id(version_id):
        """根据 ID 获取版本"""
        return Version.query.get(version_id)
    
    @staticmethod
    def get_versions_by_product(product_id, page=1, per_page=20, status=None):
        """获取指定产品的所有版本，支持分页和状态过滤"""
        query = Version.query.filter_by(product_id=product_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(Version.created_at.desc()).paginate(page=page, per_page=per_page)
    
    @staticmethod
    def update_version(version_id, **kwargs):
        """更新版本信息"""
        version = Version.query.get(version_id)
        if not version:
            return None
        
        for key, value in kwargs.items():
            if hasattr(version, key):
                setattr(version, key, value)
        
        db.session.commit()
        return version
    
    @staticmethod
    def release_version(version_id):
        """发布版本"""
        version = Version.query.get(version_id)
        if not version:
            return None
        
        version.status = 'released'
        version.released_at = datetime.utcnow()
        db.session.commit()
        return version
    
    @staticmethod
    def deprecate_version(version_id):
        """废弃版本"""
        version = Version.query.get(version_id)
        if not version:
            return None
        
        version.status = 'deprecated'
        db.session.commit()
        return version
    
    @staticmethod
    def delete_version(version_id):
        """删除版本"""
        version = Version.query.get(version_id)
        if not version:
            return False
        
        # 检查是否有关联的文件
        if version.files.count() > 0:
            return False
        
        db.session.delete(version)
        db.session.commit()
        return True
    
    @staticmethod
    def get_all_versions(page=1, per_page=20, status=None):
        """获取所有版本，支持分页和状态过滤"""
        query = Version.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Version.created_at.desc()).paginate(page=page, per_page=per_page)