import queue

import requests


class ProxyReader:

    def __init__(self):
        self.q = queue.Queue()
        self.valid_proxies = []

    def read_proxies(self):
        with open("http_proxy/proxy_list.txt", "r") as f:
            proxies = f.read().split("\n")
            for p in proxies:
                self.q.put(p)

        return self.q

    def get_valid_proxy_list(self):
        return self.valid_proxies

    def check_proxies(self):
        q = self.read_proxies()
        while not q.empty():
            proxy = q.get()
            try:
                res = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy})
            except:
                continue
            if res.status_code == 200:
                self.valid_proxies.append(proxy)
