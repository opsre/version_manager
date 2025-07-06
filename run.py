import os
from app import create_app
from app.extensions import db
from flask_migrate import upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # 迁移数据库到最新版本
    upgrade()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)