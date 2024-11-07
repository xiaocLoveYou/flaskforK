from flask import Blueprint

# 创建 auth 蓝本
auth_bp = Blueprint('auth', __name__)

# 导入 routes 文件来定义路由
from . import routes
