from flask import Blueprint

# 创建 discord 蓝本
discord_bp = Blueprint('discord', __name__)

# 导入 routes 文件来定义路由
from . import routes
