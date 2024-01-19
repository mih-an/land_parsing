import requests

ip = '31.28.11.181:41552'
login = 'Megafon1527_2'
password = 'AzsILk'

proxies = {
    'https': f'{login}:{password}@{ip}'
}

print(proxies)
url = "https://ipinfo.io/json"
response = requests.get(url=url, proxies=proxies)
print(response.text)