import pyautogui as pag
from datetime import datetime as dt
import pandas as pd
import json

df = pd.DataFrame({'A': [10, 20, 30], 'B': [100, 200, 300], 'C': ['2021-07-01', '2021-07-02', '2021-07-03']})
df['stock_code'] = '000000'
df['stock_name'] = '삼성전자'
df['C'] = pd.to_datetime(df['C'], format='%Y-%m-%d')

def fct(row):
    print(str(row['C'].date()))

df.apply(fct, axis='columns')
print(df)

print(dt.now().date())