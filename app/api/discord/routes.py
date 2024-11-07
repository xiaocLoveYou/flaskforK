from utils import *
from . import discord_bp
from flask import jsonify, request


# 获取discord信息并返回
@discord_bp.route('/getinfo', methods=['GET'])
def getinfo():
    code = request.args.get('code')
    print("discord code:", code)

    if not code:
        return jsonify({"code": 400, "messages": "缺少Code信息！"}), 200

    # authorization_header = request.headers.get("Authorization").replace("Bearer ", "")
    # print(authorization_header)
    # status, user_info = get_token(authorization_header)

    # if not status:
    #     return jsonify({"code": 400, "messages": user_info}), 200

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
    return jsonify({"code": 200, "messages": "操作成功", "data": res})

# 获取discord信息并录入
@discord_bp.route('/setinfo', methods=['GET'])
def setinfo():
    code = request.args.get('code')
    print("discord code:", code)

    if not code:
        return jsonify({"code": 400, "messages": "缺少Code信息！"}), 200

    # 获取discord token
    res = discord_exchange_code(code, "http://localhost:5500/binding.html")
    print("discord token:", res)
    if not res:
        return jsonify({"code": 500, "messages": "code失效"}), 200

    # 获取discord usee info
    res = discord_get_user_info(res["access_token"])
    print("discord info", res)
    if res == False:
        print({"code": 500, "message": "未知错误，请重试"})
        return jsonify({"code": 500, "message": "未知错误，请重试"}), 200

    authorization_header = request.headers.get("Authorization").replace("Bearer ", "")
    print(authorization_header)
    status, user_info = get_token(authorization_header)

    if not status:
        return jsonify({"code": 400, "messages": user_info}), 200

    query = """
        UPDATE users
        SET discord_id = %s,
            discord_username = %s,
            discord_avatar = %s,
            discord_global_name = %s,
            discord_locale = %s
        WHERE id = %s
    """

    params = (
        res['id'],
        res['username'],
        res['avatar'],
        res['global_name'],
        res['locale'],
        user_info['user_id']
    )

    # 调用 execute_update_query 函数
    success = execute_update_query(query, params)

    if not success:
        return jsonify({"code": 500, "message": "数据库插入失败，请重试"}), 200

    return jsonify({"code": 200, "message": "操作成功"}), 200
