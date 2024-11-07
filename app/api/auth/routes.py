import os

from . import auth_bp
from flask import jsonify, request, current_app
from utils import *


# 用户注册
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    repassword = data.get('repassword')

    if repassword != password:
        return jsonify({"code": 500, "message": "密码与验证密码不一致"}), 200

    res = execute_sql_query(f"select * from users where username = %s", (username))
    if len(res) != 0:
        return jsonify({"code": 500, "message": "用户名已被注册，请尝试其他用户名"}), 200
    res = execute_insert_query(f"insert into users(username, password, staff, tag, nickname) values(%s, password(%s), null, 'users', %s);",(username, password, username))
    print(res)

    res = execute_sql_query(f"select * from users where username = %s and password = password(%s)", (username, password))[0]
    # 获取token并返回
    info = {
        "user_id": res["id"],
        "user_name": res["username"],
        "nick_name": res["nickname"],
        "staff": res["staff"],
        "tag": res["tag"],
    }

    token: str = set_token(info)

    # 返回用户信息
    return jsonify({"code": 200, "username": username, "message": "Registered successfully", "token": token}), 200

# 用户登录
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # 假设登录成功，返回一个令牌

    res = execute_sql_query(f"select * from users where username = %s and password = password(%s)", (username, password))
    # print(res)
    if len(res) == 0:
        return jsonify({"code": 500, "message": "登录失败, 用户不存在或密码错误"}), 200
    print(res)
    res = res[0]
    info = {
        "user_id": res["id"],
        "user_name": res["username"],
        "nick_name": res["nickname"],
        "staff": res["staff"],
        "tag": res["tag"],
    }

    token: str = set_token(info)
    return jsonify({"code": 200, "message": "登录成功", "token": token}), 200

# 通过discord 快捷登录
@auth_bp.route('/loginWithDiscord', methods=['GET'])
def loginWithDiscord():
    code = request.args.get('code')
    print("discord code:", code)

    if not code:
        return jsonify({"code": 400, "messages": "缺少Code信息！"}), 200

    # 获取discord token
    res = discord_exchange_code(code)
    print("discord token:", res)
    if not res:
        return jsonify({"code": 500, "messages": "code失效"}), 200

    # 获取discord usee info
    res = discord_get_user_info(res["access_token"])
    print("discord info", res)
    if res == False:
        print({"code": 500, "message": "未知错误，请重试"})
        return jsonify({"code": 500, "message": "未知错误，请重试"}), 200

    res = execute_sql_query(f"select * from users where discord_id = %s", (res['id']))

    print(res)

    if len(res) == 0:
        return jsonify({"code": 500, "message": "登录失败, 用户不存在"}), 200
    print(res)
    res = res[0]
    info = {
        "user_id": res["id"],
        "user_name": res["username"],
        "nick_name": res["nickname"],
        "staff": res["staff"],
        "tag": res["tag"],
    }

    token: str = set_token(info)
    return jsonify({"code": 200, "message": "登录成功", "token": token}), 200

@auth_bp.route('/changePassword', methods=['put'])
def changePassword():
    data = request.get_json()
    password = data.get('password')
    newpassword = data.get("newpassword")
    renewpassword = data.get("renewpassword")

    if newpassword != renewpassword:
        return jsonify({"code": 500, "messages": "两次密码不一致"}), 200

    authorization_header = request.headers.get("Authorization").replace("Bearer ", "")
    status, user_info = get_token(authorization_header)
    if not status:
        return jsonify({"code": 401, "messages": "验证失败，请重新登录"}), 200

    user_id = user_info["user_id"]

    res = execute_update_query("update users set password = PASSWORD(%s) where id = %s", (newpassword, user_id))
    print(res)
    if not res:
        return jsonify({"code": 500, "messages": "修改失败，请重试或联系管理员"}), 200

    return jsonify({"code": 200, "messages": "操作成功"}), 200


@auth_bp.route('/upload', methods=['POST'])
def upload_file():
    """处理通过 FormData 上传的文件"""
    if 'file' not in request.files:
        return jsonify({'status': 'fail', 'message': '没有文件部分'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': 'fail', 'message': '没有选择文件'}), 400

    if file and allowed_file(file.filename):
        try:
            # 生成唯一的文件名
            unique_filename = generate_unique_filename(file.stream, file.filename)

            # 构建文件路径，使用 current_app.config
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

            # 保存文件
            file.save(file_path)

            return jsonify({
                'status': 'success',
                'message': '文件上传成功',
                'filename': unique_filename,
                'file_url': f"/uploads/{unique_filename}"
            }), 200
        except Exception as e:
            return jsonify({'status': 'fail', 'message': f'文件上传失败: {str(e)}'}), 500
    else:
        return jsonify({'status': 'fail', 'message': '不允许的文件类型'}), 400

# # 用户使用discord注册
# @auth_bp.route('/registerWithDiscord', methods=['get'])
# def registerWithDiscord():
#     code = request.args.get('code')
#     print("discord code:", code)
#
#     if not code:
#         return jsonify({"code": 400, "messages": "缺少Code信息！"}), 200
#
#     # 获取discord token
#     res = discord_exchange_code(code)
#     print("discord token:", res)
#     if not res:
#         return jsonify({"code": 500, "messages": "code失效"}), 200
#
#     # 获取discord usee info
#     res = discord_get_user_info(res["access_token"])
#     print("discord info", res)
#     if res == False:
#         print({"code": 500, "message": "未知错误，请重试"})
#         return jsonify({"code": 500, "message": "未知错误，请重试"}), 200
#
#

