from urllib.request import urlopen


class SimpleUrlReader:
    @staticmethod
    def read_url(url: str):
        page = urlopen(url)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        return html

    @staticmethod
    def get_simple_title(html):
        title_index = html.find("<title>")
        start_index = title_index + len("<title>")
        end_index = html.find("</title>")
        title = html[start_index:end_index]
        return title
