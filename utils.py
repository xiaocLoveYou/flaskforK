import hashlib

import pymysql
from pymysql import MySQLError
import jwt
import pymysql
import datetime
import requests

# discord app信息
API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1293198382105362465'
CLIENT_SECRET = 'Vv8N59jWFMUHxBhwb6VaTV83DJ39hsYD'
# REDIRECT_URI = 'http://localhost:5500/logined.html'

# 密钥，用于签名和验证JWT
secret_key = 'KKNODICK'

# 配置MYSQL信息
host = 'localhost'  # MySQL服务器地址
user = 'root'  # 用户名
password = '123456'  # 密码
database = 'laok'  # 数据库名
# query = f"SELECT * FROM users where username = 'admin' and password = password('123456')"

# MYSQL 修改数据函数
def execute_update_query(query, params):
    connection = None
    success = False
    try:
        # 连接到 MySQL 数据库
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        with connection.cursor() as cursor:
            # 如果有提供 params 参数，执行更新语句时会用 params 替代 query 中的占位符
            cursor.execute(query, params)
            connection.commit()  # 提交事务

            # 如果执行影响的行数大于0，表示更新成功
            if cursor.rowcount > 0:
                success = True
            else:
                success = False

    except MySQLError as e:
        print(f"数据库错误类型: {type(e)}")
        print(f"数据库错误信息: {e}")
        success = False
    except Exception as e:
        print(f"其他错误类型: {type(e)}")
        print(f"错误信息: {e}")
        success = False
    finally:
        # 确保连接关闭
        if connection:
            connection.close()

    return success

# MYSQL 语句插入函数
def execute_insert_query(query, params):
    connection = None
    success = False
    try:
        # 连接到 MySQL 数据库
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        with connection.cursor() as cursor:
            cursor.execute(query, params)  # 执行插入语句，params 用来传递 SQL 参数
            connection.commit()  # 提交事务

            # 如果执行影响的行数大于0，表示插入成功
            if cursor.rowcount > 0:
                success = True
            else:
                success = False

    except MySQLError as e:
        print(f"数据库错误类型: {type(e)}")
        print(f"数据库错误信息: {e}")
        success = False
    except Exception as e:
        print(f"其他错误类型: {type(e)}")
        print(f"错误信息: {e}")
        success = False
    finally:
        # 确保连接关闭
        if connection:
            connection.close()

    return success


# MYSQL 语句查询函数
def execute_sql_query(query, params):
    connection = None  # 初始化 connection 为 None
    try:
        # 连接到 MySQL 数据库
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # 返回字典形式的结果
            cursor.execute(query, params)

            # 获取所有查询结果
            result = cursor.fetchall()
            return result  # 返回查询结果，以字典的形式
    except Exception as e:
        print(f"错误类型: {type(e)}")
        print(f"错误信息: {e}")
        return None
    finally:
        # 确保连接已关闭（只有连接成功后才会关闭）
        if connection:
            connection.close()


# print(execute_sql_query(query))

# 创建token函数
def set_token(info: dict):
    # token失效时间
    info["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    # 生成JWT
    token = jwt.encode(info, secret_key, algorithm='HS256')
    print('Generated JWT:', token)
    return token


def get_token(token: str):
    try:
        # 验证JWT
        decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        print('验证成功: ', decoded_payload)
        return True, decoded_payload
    except jwt.ExpiredSignatureError:
        print('登录以过期，请重新登录')
        return False, "登录以过期，请重新登录"
    except jwt.InvalidTokenError:
        print('无效的验证信息')
        return False, "无效的验证信息"

# 使token失效
# def logout(token):
#     decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
#     BLACKLIST.add(decoded['jti'])


# 获取discord信息
def discord_exchange_code(code, REDIRECT_URI = "http://localhost:5500/logined.html"):
    print(REDIRECT_URI)
    try:
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
        r.raise_for_status()
        return r.json()
    except:
        return False


# 交换获取令牌
def discord_refresh_token(refresh_token):
    try:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
        r.raise_for_status()
        return r.json()
    except:
        return False

# 获取discord用户信息
def discord_get_user_info(token):
    header = {
        "Authorization": f"Bearer {token}"
    }
    try:
        result = requests.get("https://discord.com/api/v10/users/@me", headers=header)
        # 检查返回的状态码
        # print(result.json())
        if result.status_code == 200:
            return result.json()  # 返回成功获取的用户信息
        else:
            return False  # 如果状态码不是 200，返回 False
    except requests.exceptions.RequestException as e:
        # 捕获请求异常（如网络错误等）
        print(f"请求失败: {e}")
        return False  # 返回 False 表示请求失败


def allowed_file(filename):
    return True


def generate_unique_filename(file_stream, original_filename):
    ext = original_filename.rsplit('.', 1)[1].lower()

    # 读取文件内容并生成哈希值
    file_stream.seek(0)
    file_content = file_stream.read()
    hash_object = hashlib.sha256(file_content)
    hash_hex = hash_object.hexdigest()

    date_str = datetime.datetime.utcnow().strftime('%Y%m%d')  # 正确调用 datetime.now()
    new_filename = f"{date_str}_{hash_hex}.{ext}"
    file_stream.seek(0)
    return new_filename


def get_local_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_Authorization(request):
    try:
        return request.headers.get("Authorization").replace("Bearer ", "")
    except:
        return False
