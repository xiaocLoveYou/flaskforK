from flask import Blueprint

# 创建 blog 蓝本
blog_bp = Blueprint('blog', __name__)

# 导入 routes 文件来定义路由
from . import routes
