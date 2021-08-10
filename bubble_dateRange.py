import requests, json

url = 'http://localhost:52222/api/stock/000000/extent/'
res = requests.get(url)
if res.status_code == 200:
    print(json.loads(res.text))
else:
    print(res.status_code, res.text)