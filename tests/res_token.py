import jwt
import datetime

# 密钥，用于验证JWT
secret_key = 'KKNODICK'

# 待验证的JWT
received_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9obl9kb2UiLCJleHAiOjE3MzA4NjEzMjF9.g1YGP48oxzEIRRbRnwsbxwREeFZ44YVAsPfgDZji-Zg'

try:
    # 验证JWT
    decoded_payload = jwt.decode(received_token, secret_key, algorithms=['HS256'])
    print('Decoded Payload:', decoded_payload)
except jwt.ExpiredSignatureError:
    print('JWT has expired.')
except jwt.InvalidTokenError:
    print('Invalid JWT.')
