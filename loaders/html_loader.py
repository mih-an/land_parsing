import cloudscraper


class HtmlLoader:
    def __init__(self):
        self.url = None
        self.session = cloudscraper.create_scraper()
        self.session.headers = {'Accept-Language': 'en'}

    def load_page(self, url: str):
        self.url = url

        result = self.session.get(url=self.url)
        result.raise_for_status()

        return result

    def set_proxies(self, proxies):
        self.session.proxies = proxies

    def get_session(self):
        return self.session
