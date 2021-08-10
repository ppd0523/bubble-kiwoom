from datetime import datetime as dt
import requests
from collections import deque
from pykiwoom.kiwoom import *
# pywinauto as pwa
# pyautogui as pag
import global_var
import json
from sslog.logger import SimpleLogger
logger = SimpleLogger()

logger.info('키움앱 시작')

# 키움 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
if kiwoom.GetConnectState():
    logger.info('키움 로그인 성공')
else:
    msg = '키움 로그인 실패'
    logger.fatal(msg)
    raise Exception(msg)

# django 로그인
url = global_var.HOST + "/auth/login/"
data = {"username": global_var.DJANGO_USER, "password": global_var.DJANGO_PASSWORD}
headers_nokey = {'Content-Type': 'application/json; charset=utf-8'}
res = requests.post(url, data=json.dumps(data), headers=headers_nokey)
if res.status_code//100 != 2:
    msg = f'장고 로그인 실패. {res.status_code} {res.text}'
    logger.fatal(msg)
    raise Exception(msg)

data = json.loads(res.text)
headers_key = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f"Token {data['key']}"}
logger.info('장고 로그인 성공')

# 조건식을 PC로 다운로드, 읽기
kiwoom.GetConditionLoad()
conditions = kiwoom.GetConditionNameList()  # [(filter_id, filter_title), ...]
logger.info('키움 조건식 다운로드 성공')
logger.debug(f'{conditions}')

# django 조건식 리스트 얻기
url = global_var.HOST + '/api/filter/'
res = requests.get(url)
if res.status_code//100 != 2:
    msg = '장고 조건식 다운로드 실패'
    logger.error(f'{msg}. {res.status_code} {res.text}')
    # 조건식 획득 실패
    raise Exception(msg)

django_conditions = json.loads(res.text)
logger.info('장고 조건식 다운로드 성공')
logger.debug(django_conditions)

# 조건식 변경사항 업데이트
for cond, django_cond in zip(conditions, django_conditions):
    if cond[1] != django_cond['filter_name']:
        filter_name = django_cond['filter_name']

        django_cond['filter_name'] = cond[1]
        django_cond['filter_title'] = cond[1]
        django_cond['filter_date'] = dt.now().strftime('%Y-%m-%d')
        url = global_var.HOST + f'/api/filter/{cond[0]}/'
        res = requests.put(url, data=json.dumps(django_cond), headers=headers_key)
        if res.status_code//100 != 2:
            msg = f'조건식 업데이트 실패. {cond[0]}: {filter_name} -x {cond[1]}. {res.status_code} {res.text}({url}).'
            logger.error(msg)
            raise Exception(msg)

        logger.info(f'조건식 업데이트 성공. {cond[0]}: {filter_name} -> {cond[1]}')

# 더 많은 쪽의 조건식 제거하기
conditions_size = len(conditions)
django_conditions_size = len(django_conditions)

if conditions_size > django_conditions_size:
    # 키움쪽이 더 많으면
    for cond in conditions[django_conditions_size:]:
        data = {
            'filter_id': cond[0],
            'filter_name': cond[1],
            'filter_title': cond[1],
            'filter_date': dt.now().strftime('%Y-%m-%d')
        }
        url = global_var.HOST + f'/api/filter/{cond[0]}/'
        res = requests.post(url, data=json.dumps(data), headers=headers_key)
        if res.status_code//100 != 2:
            msg = f'조건식 추가 실패. {cond[0]}: {filter_name} -x {cond[1]}. {res.status_code} {res.text}({url}).'
            logger.error(msg)
            raise Exception(msg)

        logger.info(f'조건식 추가 성공. {cond[0]}: {cond[1]}.')

elif conditions_size < django_conditions_size:
    # 장고쪽이 더 많으면
    for django_cond in django_conditions[conditions_size:]:
        url = global_var.HOST + f'/api/filter/{cond[0]}/'
        requests.delete(url, headers=headers_key)
        if res.status_code//100 != 2:
            msg = f'조건식 삭제 실패. {cond[0]}: {filter_name} -x {cond[1]}. {res.status_code} {res.text}({url}).'
            logger.error(msg)
            raise Exception(msg)

        logger.info(f'조건식 추가 성공. {cond[0]}: {cond[1]}.')


# 조건식 검색 결과 획득
stocks = {}
for filter_id, filter_name in conditions[:2]:
    # 조건식의 종목명 리스트 획득
    codes = kiwoom.SendCondition("0101", filter_name, filter_id, 0)
    logger.info(f'{filter_id} 조건검색식 결과 종목코드 획득')
    stocks[filter_id] = [(code, kiwoom.GetMasterCodeName(code)) for code in codes]     # stocks: [(code, name), ...]
    logger.info('조건검색식 결과 종목명 획득')
logger.debug(f'{filter_id} {filter_name}: {stocks}')

for filter_id, stock_list in stocks.items():
    today = dt.now().strftime("%Y-%m-%d")
    url = global_var.HOST + f'/api/filter/{filter_id}/report/{today}/'
    data = {
        'filter_id': filter_id,
        'stock_codes': [t[0] for t in stock_list],
        'stock_names': [t[1] for t in stock_list]
    }
    res = requests.post(url, data=json.dumps(data), headers=headers_key)
    if res.status_code//100 != 2:
        msg = f'조건검색 결과 업데이트 실패. {filter_id}. {res.status_code} {res.text}'
        logger.warning(msg)
    else:
        msg = f'조건검색 결과 업데이트 성공. {filter_id}.)'
        logger.info(msg)


# 일봉 차트 조회 준비
prices = []
def _appendData(code, name):
    def inner(row):
        d = {
            'stock_code': code,
            'stock_name': name,
            'date': str(row['일자'].date()),
            'high_price': int(row['고가']),
            'low_price': int(row['저가']),
            'open_price': int(row['시가']),
            'close_price': int(row['현재가']),
            'adj_close_price': int(row['현재가']),
            'volume': int(row['거래량']),
        }
        prices.append(d)

    return inner


# 일봉 차트 조회
for filter_id, stock_list in stocks.items():
    # 장고에서 일봉 차트 조회
    for code, name in stock_list:
        url = global_var.HOST + f'/api/stock/{code}/extent/'
        res = requests.get(url)
        if res.status_code//100 != 2:
            msg = f'{code} {name} 일봉차트 범위 조회 실패. {res.status_code} {res.text}.'
            logger.warning(msg)
            raise Exception(msg)

        data = json.loads(res.text)
        begin = data['begin_date']  # 과거
        end = data['end_date']  # 최근
        logger.debug(f'{code} {name} 일봉차트 범위 조회 성공.')

        df = kiwoom.block_request("opt10081", 종목코드=code, 수정주가구분=1, output="주식일봉차트조회", next=0)

        # 장고에 일봉이 없으면
        if (not begin) and (not end):
            dfs = deque([df])
            # column : [종목코드, 현재가, 거래량, 거래대금, 일자, 시가, 고가, 저가, 수정주가구분, 수정비율, 대업종구분, 소업종구분, 종목정보, 수정주가이벤트, 전일종가]

            _append = dfs.appendleft
            while kiwoom.tr_remained:
                df = kiwoom.block_request("opt10081", 종목코드=code, 수정주가구분=1, output="주식일봉차트조회", next=2)
                _append(df)
                logger.debug(f'{code} {name} 일봉 조회 {min(df["일자"])} - {max(df["일자"])}')

            df = pd.concat(list(dfs), ignore_index=True)
            # df['일자'] = df['일자'].map(lambda x: pd.to_datetime(x, format='%Y%m%d')) # 키움날짜 표시 yyyymmdd

        # else:
        #     df['일자'] = df['일자'].map(lambda x: pd.to_datetime(x, format='%Y%m%d'))
        #     df = df[end < df['일자']]  # 최신 데이터만 획득

        df['일자'] = df['일자'].map(lambda x: pd.to_datetime(x, format='%Y%m%d'))
        if end:
            df = df[end < df['일자']]  # 최신 데이터만 획득

        funct = _appendData(code, name)
        df.apply(funct, axis='columns')

        url = f'{global_var.HOST}/api/stock/{code}/price/'
        res = requests.post(url, data=json.dumps({'stocks': prices, 'date': str(dt.now().date())}), headers=headers_key)
        if res.status_code//100 != 2:
            msg = f'{code} {name} 일봉 업데이트 실패 {res.status_code} {res.text}'
            logger.warning(msg)
        else:
            logger.debug(f'{code} {name} 일봉 업데이트 성공')


logger.info(f'키움앱 완료')
# end for code, name in stocks