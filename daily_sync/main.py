import os
import requests
from requests.auth import HTTPBasicAuth
import sys
from pathlib import Path

# WebDAV サーバアドレス
WEBDAV_SERVER_ADDRESS = os.environ.get('WEBDAV_SERVER_ADDRESS')
KABU_PLUS_ID = os.environ.get('KABU_PLUS_ID')
KABU_PLUS_PW = os.environ.get('KABU_PLUS_PW')
OUTPUT_PATH = os.environ.get('OUTPUT_PATH', '.')

ENDPOINT = os.environ.get('ENDPOINT', 
    'https://csvex.com/kabu.plus/csv/japan-all-stock-prices/daily/japan-all-stock-prices.csv')
UA = f'Auto sync program executed by {KABU_PLUS_ID}'
AUTH = HTTPBasicAuth(KABU_PLUS_ID, KABU_PLUS_PW)
HEADERS = {
    'User-Agent': UA,
    'Accept-Encoding': 'gzip',
}

def main() -> str:
    resp = requests.get(ENDPOINT, auth=AUTH)
    resp.encoding = resp.apparent_encoding
    if resp.status_code == 200:
        csv = resp.content.decode('s_jis')
        path = Path(OUTPUT_PATH) / 'current.csv'
        with open(str(path), 'w') as f:
            f.write(csv)
            return csv

    else:
        from pprint import PrettyPrinter
        pp = PrettyPrinter()
        print(f'[{resp.status_code}]')
        pp.pprint(resp)
        sys.exit(1)

csv = main()
sys.exit(0)