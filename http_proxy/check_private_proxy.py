import time
from datetime import datetime
from loaders.html_loader import HtmlLoader

# ip = '31.28.11.181:41552'
# login = 'Megafon1527_2'
# password = 'AzsILk'
ip = '176.9.154.69:7837'
login = 'taoqAQbvcD'
password = '8drob10Mgi'

proxies = {
    'http': f'{login}:{password}@{ip}'
}

print(proxies)
url = "https://ipinfo.io/json"

land_parser = HtmlLoader()
land_parser.set_proxies(proxies)

index = 0
while index < 100:
    try:
        resp = land_parser.load_page(url)
        print(f'Loop cycle number: {index}')
        print(resp.text)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        print('Sleeping for 10 seconds...')
        time.sleep(10)
        index += 1

    except Exception as exc:
        print(f"Failed: {exc}")
        print('Sleeping for 10 seconds...')
        time.sleep(10)
