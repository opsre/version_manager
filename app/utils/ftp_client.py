import os
import ftplib
from flask import current_app
import uuid
import traceback

class FTPClient:
    def __init__(self):
        self.host = current_app.config['FTP_HOST']
        self.port = current_app.config['FTP_PORT']
        self.username = current_app.config['FTP_USERNAME']
        self.password = current_app.config['FTP_PASSWORD']
        self.directory = current_app.config['FTP_DIRECTORY']
        self.ftp = None
        print(f"FTP配置: {self.host}:{self.port}, 用户名: {self.username}, 目录: {self.directory}")
    
    def connect(self):
        """连接到 FTP 服务器"""
        try:
            print(f"正在连接FTP服务器 {self.host}:{self.port}...")
            self.ftp = ftplib.FTP()
            self.ftp.connect(self.host, self.port)
            print(f"连接成功，正在登录...")
            self.ftp.login(self.username, self.password)
            print(f"登录成功")
            
            # 尝试切换到指定目录，如果不存在则创建
            try:
                self.ftp.cwd(self.directory)
                print(f"已切换到目录: {self.directory}")
            except ftplib.error_perm as e:
                print(f"目录不存在，创建目录: {self.directory}, 错误: {str(e)}")
                # 目录不存在，创建目录
                self._create_directory_tree(self.directory)
                self.ftp.cwd(self.directory)
                print(f"目录创建成功并切换到: {self.directory}")
                
            return True
        except Exception as e:
            print(f"FTP 连接错误: {str(e)}")
            traceback.print_exc()
            return False
    
    def _create_directory_tree(self, directory):
        """递归创建目录树"""
        if directory == '/':
            return
        
        parent = os.path.dirname(directory)
        if parent and parent != '/':
            try:
                self.ftp.cwd(parent)
            except ftplib.error_perm:
                self._create_directory_tree(parent)
                self.ftp.cwd(parent)
        
        try:
            self.ftp.mkd(os.path.basename(directory))
        except ftplib.error_perm:
            pass  # 目录可能已存在
    
    def disconnect(self):
        """断开 FTP 连接"""
        if self.ftp:
            self.ftp.quit()
            self.ftp = None
            print("FTP连接已断开")
    
    def upload_file(self, file_data, original_filename, version_id):
        """上传文件到 FTP 服务器"""
        print(f"准备上传文件: {original_filename}, 版本ID: {version_id}")
        if not self.connect():
            print("FTP连接失败，上传中止")
            return None
        
        try:
            # 创建版本目录
            version_dir = f"version_{version_id}"
            try:
                self.ftp.cwd(version_dir)
                print(f"已切换到版本目录: {version_dir}")
            except ftplib.error_perm:
                print(f"版本目录不存在，创建: {version_dir}")
                self.ftp.mkd(version_dir)
                self.ftp.cwd(version_dir)
                print(f"版本目录创建成功")
            
            # 检查并生成不重复的文件名
            name, ext = os.path.splitext(original_filename)
            filename = original_filename
            counter = 1
            while self._is_file_exists(self.ftp, filename):
                filename = f"{name}{counter}{ext}"
                counter += 1
            
            # 上传文件
            print("开始上传文件...")
            self.ftp.storbinary(f'STOR {filename}', file_data)
            print("文件上传完成")
            
            # 返回文件路径
            file_path = f"{self.directory}/{version_dir}/{filename}"
            print(f"文件上传路径: {file_path}")
            return {
                'filename': filename,
                'original_filename': original_filename,
                'file_path': file_path
            }
        except Exception as e:
            print(f"文件上传错误: {str(e)}")
            traceback.print_exc()
            return None
        finally:
            self.disconnect()
    
    @staticmethod
    def _is_file_exists(ftp, filename):
        """检查文件是否存在"""
        try:
            # 获取目录中的文件列表
            files = []
            ftp.retrlines('LIST', files.append)
            print(f"目录中的文件列表: {files}")
            
            # 检查文件是否在列表中
            for file_info in files:
                if filename in file_info:
                    print(f"文件 {filename} 存在于FTP服务器")
                    return True
            
            print(f"文件 {filename} 不存在于FTP服务器")
            return False
        except Exception as e:
            print(f"检查文件存在性时出错: {str(e)}")
            return False
    
    def download_file(self, file_path):
        """从 FTP 服务器下载文件"""
        print(f"准备下载文件: {file_path}")
        if not self.connect():
            print("FTP连接失败，下载中止")
            return None
        
        try:
            # 提取相对于self.directory的子目录
            rel_path = os.path.relpath(file_path, self.directory)
            directory = os.path.dirname(rel_path)
            filename = os.path.basename(file_path)
            print(f"相对目录: {directory}, 文件名: {filename}")
            # 切换到文件所在目录
            if directory and directory != '.':
                print(f"切换到目录: {directory}")
                try:
                    self.ftp.cwd(directory)
                    print(f"已切换到目录: {directory}")
                except ftplib.error_perm as e:
                    print(f"目录不存在或无法访问: {directory}, 错误: {str(e)}")
                    return None
            # 检查文件是否存在
            if not self._is_file_exists(self.ftp, filename):
                return None
            # 创建内存文件对象
            from io import BytesIO
            file_data = BytesIO()
            # 下载文件
            print(f"开始下载文件...")
            try:
                self.ftp.retrbinary(f'RETR {filename}', file_data.write)
                print(f"文件下载完成")
            except ftplib.error_perm as e:
                print(f"下载文件时出错: {str(e)}")
                return None
            # 将文件指针移到开始位置
            file_data.seek(0)
            return file_data
        except Exception as e:
            print(f"文件下载错误: {str(e)}")
            traceback.print_exc()
            return None
        finally:
            self.disconnect()

    def delete_file(self, file_path):
        """从FTP服务器删除文件"""
        print(f"准备删除FTP文件: {file_path}")
        if not self.connect():
            print("FTP连接失败，删除中止")
            return False
        try:
            # 提取相对于self.directory的子目录
            rel_path = os.path.relpath(file_path, self.directory)
            directory = os.path.dirname(rel_path)
            filename = os.path.basename(file_path)
            print(f"相对目录: {directory}, 文件名: {filename}")
            # 切换到文件所在目录
            if directory and directory != '.':
                try:
                    self.ftp.cwd(directory)
                    print(f"已切换到目录: {directory}")
                except ftplib.error_perm as e:
                    print(f"目录不存在或无法访问: {directory}, 错误: {str(e)}")
                    return False
            # 删除文件
            self.ftp.delete(filename)
            print(f"FTP文件已删除: {filename}")
            return True
        except Exception as e:
            print(f"FTP删除文件失败: {str(e)}")
            return False
        finally:
            self.disconnect()