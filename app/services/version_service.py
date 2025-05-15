# 导入操作系统模块，用于文件操作
import os
# 导入版本数据模型
from app.models.version import Version
# 导入数据库实例
from app.extensions import db
# 导入日志记录器
from loguru import logger


class VersionService:
    """
    版本管理服务类
    
    提供版本信息的增删改查以及文件上传下载等功能
    """
    
    @staticmethod
    def get_all_versions():
        """
        获取所有版本信息
        
        Returns:
            所有版本对象的列表
        """
        return Version.query.all()

    @staticmethod
    def get_version_by_id(version_id):
        """
        根据ID获取特定版本信息
        
        Args:
            version_id: 版本ID
            
        Returns:
            版本对象，若不存在则返回None
        """
        return Version.query.get(version_id)

    @staticmethod
    def get_version_by_version(version):
        """
        根据版本号获取特定版本信息
        
        Args:
            version: 版本号
            
        Returns:
            版本对象，若不存在则返回None
        """
        return Version.query.filter_by(version=version).first()

    @staticmethod
    def create_version(version_data, file=None):
        """
        创建新版本
        
        Args:
            version_data: 包含版本信息的字典
            file: 可选，上传的文件对象
            
        Returns:
            创建的版本对象
            
        Raises:
            Exception: 当创建版本失败时抛出
        """
        try:
            # 创建版本对象
            version = Version(
                version=version_data['version'],
                description=version_data.get('description', ''),
                file_path=version_data.get('file_path', '')
            )

            # 如果提供了文件，则保存文件
            if file:
                # 生成文件名（版本号_原始文件名）
                filename = f"{version.version}_{file.filename}"
                # 构建文件保存路径
                file_path = os.path.join('uploads', filename)
                # 保存文件
                file.save(file_path)
                # 更新版本记录中的文件路径
                version.file_path = file_path

            # 添加到数据库会话并提交
            db.session.add(version)
            db.session.commit()
            return version
        except Exception as e:
            # 发生错误时回滚事务
            db.session.rollback()
            # 记录错误信息
            logger.error(f"Error creating version: {str(e)}")
            # 重新抛出异常，由调用方处理
            raise

    @staticmethod
    def update_version(version_id, version_data, file=None):
        """
        更新现有版本
        
        Args:
            version_id: 要更新的版本ID
            version_data: 包含新版本信息的字典
            file: 可选，新上传的文件对象
            
        Returns:
            更新后的版本对象，若版本不存在则返回None
            
        Raises:
            Exception: 当更新版本失败时抛出
        """
        try:
            # 查找要更新的版本
            version = Version.query.get(version_id)
            if not version:
                return None

            # 更新版本信息
            version.version = version_data.get('version', version.version)
            version.description = version_data.get('description', version.description)

            # 如果提供了新文件
            if file:
                # 删除旧文件（如果存在）
                if version.file_path and os.path.exists(version.file_path):
                    os.remove(version.file_path)

                # 保存新文件
                filename = f"{version.version}_{file.filename}"
                file_path = os.path.join('uploads', filename)
                file.save(file_path)
                version.file_path = file_path

            # 提交变更到数据库
            db.session.commit()
            return version
        except Exception as e:
            # 发生错误时回滚事务
            db.session.rollback()
            # 记录错误信息
            logger.error(f"Error updating version: {str(e)}")
            # 重新抛出异常，由调用方处理
            raise

    @staticmethod
    def delete_version(version_id):
        """
        删除指定版本
        
        Args:
            version_id: 要删除的版本ID
            
        Returns:
            布尔值，表示删除操作是否成功
            
        Raises:
            Exception: 当删除版本失败时抛出
        """
        try:
            # 查找要删除的版本
            version = Version.query.get(version_id)
            if not version:
                return False

            # 删除关联文件（如果存在）
            if version.file_path and os.path.exists(version.file_path):
                os.remove(version.file_path)

            # 从数据库中删除版本记录
            db.session.delete(version)
            db.session.commit()
            return True
        except Exception as e:
            # 发生错误时回滚事务
            db.session.rollback()
            # 记录错误信息
            logger.error(f"Error deleting version: {str(e)}")
            # 重新抛出异常，由调用方处理
            raise