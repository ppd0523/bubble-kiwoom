import requests, json

stock_code = '000002'
stock_name = '현대차'
date = '2021-08-31'
url = f'http://localhost:52222/api/stock/{stock_code}/price/'
data = {
    'stocks': [
        {'stock_code': '000000', 'stock_name': '현대차', 'high_price': 150000, 'low_price': 130000, 'open_price': 140000, 'close_price': 145000, 'adj_close_price': 145000, 'volume': 1000, 'date': '2021-08-01'},
        {'stock_code': '000001', 'stock_name': '삼성전자', 'high_price': 150000, 'low_price': 130000, 'open_price': 140000, 'close_price': 145000, 'adj_close_price': 145000, 'volume': 1000, 'date': '2021-08-01'},
        {'stock_code': '000002', 'stock_name': 'LG전자', 'high_price': 150000, 'low_price': 130000, 'open_price': 140000, 'close_price': 145000, 'adj_close_price': 145000, 'volume': 1000, 'date': '2021-08-01'},
    ],
    'date': date
}

headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f"Token {key}"}
res = requests.post(url, data=json.dumps(data), headers=headers)

if res.status_code == 200:
    print(res.text)
else:
    print(res.status_code, res.text)