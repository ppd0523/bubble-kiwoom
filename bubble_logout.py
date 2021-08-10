import requests, json

url = "http://localhost:52222/auth/logout/"

key = "43e11adbbd0b94466ca6e4119882ee1447e08a25"
headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f"Token {key}"}
res = requests.post(url, headers=headers)

if res.status_code == 200:
    print(res.text)
else:
    print(res.status_code, res.text)