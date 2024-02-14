import json
import requests

url = 'http://127.0.0.1:8080/powerloss/login?include_auth_token'  # 注意这里include_auth_token是以查询参数的形式出现，不能放在payload中
username = 'tempUser'
password = '123456789'

payload = {
    'username': username,
    'password': password
}

def test_token(auth_token):    
    test_token_url = f'http://127.0.0.1:8080/api/test-token?auth_token={auth_token}'
    response = requests.post(test_token_url)
    response_data = json.loads(response.text)
    print(response_data['message'])

response = requests.post(url, json=payload)
response_data = json.loads(response.text)

if response.status_code == 200:
    auth_token = response_data['response']['user']['authentication_token']    
    print("Login successful. Auth token:", auth_token)
    test_token(auth_token)
else:
    print("Login failed. Status code:", response.status_code)
    print("errors: ", response_data['response']['errors'])
