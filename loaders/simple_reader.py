from urllib.request import urlopen


class SimpleReader:
    @staticmethod
    def read_url(url: str):
        page = urlopen(url)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        return html

    def get_title(self, html):
        title_index = html.find("<title>")
        start_index = title_index + len("<title>")
        end_index = html.find("</title>")
        title = html[start_index:end_index]
        return title
