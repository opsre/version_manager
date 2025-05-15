# 导入应用工厂函数和配置对象
from app import create_app
from config.config import config

# 使用默认配置创建Flask应用实例
app = create_app(config['default'])

# 当直接运行此文件时，启动Flask开发服务器
if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],      # 服务器主机地址，从配置中获取
        port=app.config['PORT'],      # 服务器端口，从配置中获取
        debug=app.config['DEBUG']     # 是否启用调试模式，从配置中获取
    )