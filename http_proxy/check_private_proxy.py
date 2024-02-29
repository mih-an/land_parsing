
import creds
from loaders.html_loader import HtmlLoader

proxy_full_address = f'http://{creds.proxy_login}:{creds.proxy_password}@{creds.proxy_ip}'
proxies = {'http': f'{proxy_full_address}', 'https': f'{proxy_full_address}'}

print(proxies)
url = "https://ipinfo.io/json"

land_parser = HtmlLoader()
land_parser.set_proxies(proxies)

resp = land_parser.load_page(url)
print(resp.text)
