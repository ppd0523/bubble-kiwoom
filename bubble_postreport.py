import requests, json


def url_with_param(filter_id, date, stock_codes, stock_names):
    _url = f'http://localhost:52222/api/filter/{filter_id}/report/{date}/'
    _data = {
        'stock_codes': stock_codes,
        'stock_names': stock_names
    }
    return _url, _data

stock_codes = ['000000', '000001', '000002']
stock_names = ['삼성전자', 'LG전자', '현대차']
url, data = url_with_param('000', '2021-08-01', stock_codes, stock_names)

key = "43e11adbbd0b94466ca6e4119882ee1447e08a25"
headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f"Token {key}"}
res = requests.post(url, data=json.dumps(data), headers=headers)

if res.status_code == 200:
    print(res.text)
else:
    print(res.status_code, res.text)