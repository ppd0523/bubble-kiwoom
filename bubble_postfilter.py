import requests, json
import global_var

data = {
    'filter_id': "000",
    'filter_name': "새거",
    'filter_title': "가끔 저점에서 강한 수급",
    'filter_date': '2021-08-08'
}
url = global_var.HOST + '/api/filter/000/'


headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f"Token {key}"}
res = requests.put(url, data=json.dumps(data), headers=headers)

if res.status_code//100 != 2:
    print(res.text)
    raise Exception('API failed')

print(json.loads(res.text))