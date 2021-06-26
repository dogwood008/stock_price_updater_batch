from sqlite3.dbapi2 import SQLITE_DROP_TABLE
import pandas as pd
import sqlite3
import contextlib
import datetime

file_path = '/opt/csv/japan-all-stock-prices.csv'
SQLITE_DB_PATH = '/opt/csv/stocks.db'

dtype = {
    'SC': str,
    '名称': str,
    '市場': str,
    '業種': str,
    '日付': str,
    '株価': float,
    '前日比': float,
    '前日比（％）': float,
    '前日終値': float,
    '始値': float,
    '高値': float,
    '安値': float,
    '出来高': float,
    '売買代金（千円）': float,
    '時価総額（百万円）': float,
    '値幅下限': float,
    '値幅上限': float,
}

df = pd.read_csv(file_path, encoding='sjis').replace('-', 0).astype(dtype)
df['日付'] = pd.to_datetime(df['日付'] + 'T15:00:00', format='%Y%m%dT%H:%M:%S')

with contextlib.closing(sqlite3.connect(SQLITE_DB_PATH)) as con:
    with con as cur:
        df.to_sql('stocks', cur, if_exists='replace', index=False)
