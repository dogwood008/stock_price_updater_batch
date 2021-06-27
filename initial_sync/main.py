from sqlite3.dbapi2 import SQLITE_DROP_TABLE
import pandas as pd
import sqlite3
from sqlite3 import Connection
import contextlib
import glob

file_path = '/opt/csv/*.csv'
SQLITE_DB_PATH = '/opt/csv/stocks.db'
TABLE_NAME = 'stocks'

dtype = {
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

def insert(con: Connection):
    files = glob.glob(file_path)
    with con as cur:
        for i, file in enumerate(files):
            print(f'processing... %5d / %5d {file}' % (i, len(files)))
            df = pd.read_csv(file, encoding='sjis').replace('-', 0)
            if '日時' in df.columns:
                # old type
                df['日時'] = df['日時'].replace(0, '2000/1/1 00:00')
                df['日付'] = pd.to_datetime(df['日時'].astype(str), format='%Y/%m/%d %H:%M')
                df = df.drop(columns='日時')
            else:
                df['日付'] = pd.to_datetime(df['日付'].astype(str) + 'T15:00:00', format='%Y%m%dT%H:%M:%S')
            df = df.astype(dtype)
            df.index = df[['SC', '日付']]
            df.to_sql(TABLE_NAME, cur, if_exists='append', index=False)
    
def set_index(con: Connection):
    create_index = f'CREATE INDEX index_sc_date ON {TABLE_NAME}(`SC`, `日付`)'
    with con as cur:
        cur.execute(create_index)

def main():
    with contextlib.closing(sqlite3.connect(SQLITE_DB_PATH)) as con:
        insert(con)
        set_index(con)

main()