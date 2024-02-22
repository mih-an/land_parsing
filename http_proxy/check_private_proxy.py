import datetime
import time
import creds
from loaders.html_loader import HtmlLoader

proxies = {
    'http': f'{creds.proxy_login}:{creds.proxy_password}@{creds.proxy_ip}'
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
