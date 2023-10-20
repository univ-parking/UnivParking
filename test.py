import requests

url = 'http://127.0.0.1:8000/api/auth'

response = requests.post(url, data={'username': 'admin', 'password': 1234})

print(response.text)

myToken = response.json()

header = {'Authorization': 'Token '+myToken.get('token')}
response = requests.get('http://127.0.0.1:8000/api/user_list', headers=header)

print(response.text)