import os

from flask import Flask
from flask_cors import CORS
from .api.auth import auth_bp
from .api.blog import blog_bp
from .api.discord import discord_bp
from .api.temp import temp_bp


# from .api.product import product_bp


def create_app():
    app = Flask(__name__)
    # 解决跨域
    CORS(app)
    # 配置应用
    # app.config.from_pyfile('config.py')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大上传大小 16MB
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # 注册蓝本
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  # 认证 API
    app.register_blueprint(blog_bp, url_prefix='/api/blog')  # 博客 API
    app.register_blueprint(discord_bp, url_prefix='/api/discord')  # discord API
    app.register_blueprint(temp_bp, url_prefix='/api/discord')  # discord API
    # app.register_blueprint(product_bp, url_prefix='/api/product')  # 商品管理 API

    return app
