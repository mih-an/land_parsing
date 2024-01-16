import cloudscraper
import socket


class LandParser:
    def __init__(self):
        self.url = None
        self.session = cloudscraper.create_scraper()
        self.session.headers = {'Accept-Language': 'en'}

        self.result = []

    def load_page(self, url: str):
        self.url = url

        socket.setdefaulttimeout(10)
        result = self.session.get(url=self.url)
        result.raise_for_status()

        return result

    def set_proxy(self, proxy):
        self.session.proxies = {"http": proxy, "https": proxy}
