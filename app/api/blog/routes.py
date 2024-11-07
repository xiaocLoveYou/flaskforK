from utils import *
from . import blog_bp
from flask import jsonify, request

# 上传帖子
@blog_bp.route('/createpost', methods=['POST'])
def createpost():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    # img
    game = data.get("game")
    mode = data.get("mode")
    imgurl = data.get("imgurl")
    print(imgurl)
    # if imgurl is None:
    #     imgurl = "null"
    authorization = request.headers.get("Authorization").replace("Bearer ", "")
    status, info = get_token(authorization)

    if not status:
        return jsonify({
            "code": 401,
            "messages": "登录失效，请重新登录"
        }), 200

    sql = "insert into blogs(title, content, create_time, game, mode, user_id, username, imgurl) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (
        title,
        content,
        get_local_time(),
        game,
        mode,
        info["user_id"],
        info["user_name"],
        imgurl
    )

    res = execute_insert_query(sql,data)

    if not res:
        return jsonify({
            "code": 500,
            "messages": "内部错误，请联系管理员或重试"
        }), 200

    return jsonify({
            "code": 200,
            "messages": "操作成功"
        }), 200



# 删除帖子
@blog_bp.route('/delpost', methods=['GET'])
def delpost():
    id = request.args.get('id')
    authorization = request.headers.get("Authorization").replace("Bearer ", "")

    status, info = get_token(authorization)

    if not status:
        return jsonify({
            "code": 401,
            "messages": "登录失效，请重新登录"
        }), 200

    res = execute_update_query("delete from blogs where id = %s and user_id = %s", (id, info["user_id"]))

    if not res:
        return jsonify({"code": "500", "messages": "内部错误，请联系管理员或重试"}), 200

    return jsonify({
            "code": 200,
            "messages": "操作成功"
        }), 200


# 获取帖子列表
@blog_bp.route('/posts', methods=['GET'])
def posts():
    # return 123
    authorization = get_Authorization(request)

    status, info = get_token(authorization)
    if not info or not status:
        return jsonify({"code": 401, "messages": "登录验证失效，请重新登录"}), 200

    print("验证信息", info)

    res = execute_sql_query("SELECT b.*, COUNT(bl.blog_id) AS like_count, sum(bl.user_id = %s) as is_like FROM blogs b LEFT JOIN blog_likes bl ON b.id = bl.blog_id GROUP BY b.id",(info["user_id"]))

    if not res:
        return jsonify({"code": "500", "messages": "内部错误，请联系管理员或重试"}), 200

    return jsonify({
        "code": 200,
        "messages": "操作成功",
        "data": res
    }), 200

# 获取本人发布的帖子
@blog_bp.route('/myposts', methods=['GET'])
def myposts():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)
    if not info or not status:
        return jsonify({"code": 401, "messages": "登录验证失效，请重新登录"}), 200

    print("验证信息", info)

    res = execute_sql_query(
        "SELECT b.*, COUNT(bl.blog_id) AS like_count, sum(bl.user_id = %s) as is_like FROM blogs b LEFT JOIN blog_likes bl ON b.id = bl.blog_id GROUP BY b.id having b.user_id = %s",
        (info["user_id"], info["user_id"]))
    print(res)

    if not res:
        return jsonify({"code": "500", "messages": "内部错误，请联系管理员或重试"}), 200

    return jsonify({
        "code": 200,
        "messages": "操作成功",
        "data": res
    }), 200

# 获取帖子详情
@blog_bp.route('/posts/<int:post_id>', methods=['GET'])
def post():
    pass

# 帖子点赞
@blog_bp.route('/postlike', methods=['GET'])
def postlike():
    blog_id = request.args.get('blog_id')

    authorization = get_Authorization(request)

    status, info = get_token(authorization)
    if not info or not status:
        return jsonify({"code": 401, "messages": "登录验证失效，请重新登录"}), 200

    print("验证信息", info)

    res = execute_insert_query("insert into blog_likes(blog_id, user_id) values(%s, %s)", (blog_id, info["user_id"]))
    print(res)

    if not res:
        return jsonify({"code": "500", "messages": "内部错误，请联系管理员或重试"}), 200

    return jsonify({
        "code": 200,
        "messages": "操作成功",
        "data": res
    }), 200


# 帖子取消点赞
@blog_bp.route('/postunlike', methods=['GET'])
def postunlike():
    blog_id = request.args.get('blog_id')

    authorization = get_Authorization(request)

    status, info = get_token(authorization)
    if not info or not status:
        return jsonify({"code": 401, "messages": "登录验证失效，请重新登录"}), 200

    print("验证信息", info)

    res = execute_insert_query("delete from blog_likes where blog_id = %s and user_id = %s", (blog_id, info["user_id"]))
    print(res)

    if not res:
        return jsonify({"code": "500", "messages": "内部错误，请联系管理员或重试"}), 200

    return jsonify({
        "code": 200,
        "messages": "操作成功",
        "data": res
    }), 200


