import queue
import threading
from queue import Queue
from typing import Any
import requests


class ProxyReader:

    def __init__(self):
        self.q = queue.Queue()
        self.valid_proxies = []

    def read_proxies(self):
        with open("http_proxy/proxy_list.txt", "r") as file:
            proxy_list = file.read().split("\n")
            for proxy in proxy_list:
                self.q.put(proxy)

        return self.q

    def get_valid_proxy_list(self):
        return self.valid_proxies

    def check_proxies(self):
        proxy_queue = self.read_proxies()
        while not proxy_queue.empty():
            proxy = proxy_queue.get()
            try:
                res = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy})
            except:
                continue
            if res.status_code == 200:
                print(proxy + " is working")
                self.valid_proxies.append(proxy)


q: Queue[Any] = queue.Queue()

with open("proxy_list.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)


for _ in range(60):
    threading.Thread(target=check_proxies).start()
