import requests
import global_var
import json


# django 조건식 리스트 얻기
res = requests.get(global_var.HOST + '/api/filter/')
if res.status_code != 200:
    # 조건식 획득 실패
    exit(0)

print(json.loads(res.text))