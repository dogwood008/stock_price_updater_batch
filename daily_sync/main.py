import os
import requests
from requests.auth import HTTPBasicAuth
import sys
from pathlib import Path
import pandas as pd
import contextlib
import sqlite3
import datetime

# WebDAV サーバアドレス
WEBDAV_SERVER_ADDRESS = os.environ.get('WEBDAV_SERVER_ADDRESS')
KABU_PLUS_ID = os.environ.get('KABU_PLUS_ID')
KABU_PLUS_PW = os.environ.get('KABU_PLUS_PW')
OUTPUT_PATH = os.environ.get('OUTPUT_PATH', '.')

SQLITE_DB_PATH = '/opt/csv/stocks.db'
TABLE_NAME = 'stocks'

ENDPOINT = os.environ.get('ENDPOINT', 
    'https://csvex.com/kabu.plus/csv/japan-all-stock-prices/daily/japan-all-stock-prices.csv')
UA = f'Auto sync program executed by {KABU_PLUS_ID}'
AUTH = HTTPBasicAuth(KABU_PLUS_ID, KABU_PLUS_PW)
HEADERS = {
    'User-Agent': UA,
    'Accept-Encoding': 'gzip',
}

D_TYPES = {
    'SC': 'string',
    '名称': 'string',
    '市場': 'string',
    '業種': 'string',
    '日付': 'string',
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

def fetch() -> str:
    resp = requests.get(ENDPOINT, auth=AUTH)
    resp.encoding = resp.apparent_encoding
    if resp.status_code == 200:
        csv = resp.content.decode('s_jis')
        path = Path(OUTPUT_PATH) / 'current.csv'
        with open(str(path), 'w') as f:
            f.write(csv)
            return path

    else:
        from pprint import PrettyPrinter
        pp = PrettyPrinter()
        print(f'[{resp.status_code}]')
        pp.pprint(resp)
        sys.exit(1)

def get_df(dtype: dict) -> pd.DataFrame:
    csv_path = fetch()
    encoding = 'utf-8'
    df = pd.read_csv(csv_path, encoding=encoding).replace('-', 0)
    df['日付'] = pd.to_datetime(df['日付'].astype(str) + 'T15:00:00', format='%Y%m%dT%H:%M:%S')
    df = df.astype(dtype)
    df.index = df[['SC', '日付']]
    return df

def insert_into_db(df: pd.DataFrame, sqlite_db_path: str, table_name: str):
    '''
    https://stackoverflow.com/a/48562426/15983717
    '''
    with contextlib.closing(sqlite3.connect(sqlite_db_path)) as con:
        with con as cur:
            df.to_sql(TABLE_NAME, cur, if_exists='append', index=False)

def main():
    df = get_df(D_TYPES)
    insert_into_db(df, SQLITE_DB_PATH, TABLE_NAME)

main()
sys.exit(0)