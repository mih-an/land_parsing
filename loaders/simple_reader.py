from urllib.request import urlopen


class SimpleReader:
    @staticmethod
    def read_url(url: str):
        page = urlopen(url)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        return html
