import jwt
import datetime

# 密钥，用于签名和验证JWT
secret_key = 'KKNODICK'

# 载荷，即JWT中包含的信息
payload = {
    'user_id': 123,
    'username': 'john_doe',
    'exp': 1730861321
    # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
}

# 生成JWT
token = jwt.encode(payload, secret_key, algorithm='HS256')
print('Generated JWT:', token)
