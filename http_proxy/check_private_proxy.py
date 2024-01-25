
from loaders.land_parser import LandParser

ip = '31.28.11.181:41552'
login = 'Megafon1527_2'
password = 'AzsILk'

proxies = {
    'https': f'{login}:{password}@{ip}'
}

print(proxies)
url = "https://ipinfo.io/json"
land_parser = LandParser()
land_parser.set_proxies(proxies)

try:
    resp = land_parser.load_page(url)
    print(resp.text)
except:
    print("Failed")
