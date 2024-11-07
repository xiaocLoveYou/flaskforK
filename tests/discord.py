import requests

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1293198382105362465'
CLIENT_SECRET = 'Vv8N59jWFMUHxBhwb6VaTV83DJ39hsYD'
REDIRECT_URI = 'http://localhost:5500/logined.html'


def exchange_code(code):
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
