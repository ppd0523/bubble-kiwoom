import requests, json
import global_var

url = global_var.HOST + "/auth/login/"
data = {"username": global_var.USER, "password": global_var.PASSWORD}
headers = {'Content-Type': 'application/json; charset=utf-8'}
res = requests.post(url, data=json.dumps(data), headers=headers)

if res.status_code//100 != 2:
    print(res.status_code, res.text)

res = json.loads(res.text)
key = res['key']
print('로그인 성공', key)
