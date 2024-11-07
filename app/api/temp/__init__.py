from flask import Blueprint

# 创建 temp 蓝本
temp_bp = Blueprint('temp', __name__)

# 导入 routes 文件来定义路由
from . import routes
