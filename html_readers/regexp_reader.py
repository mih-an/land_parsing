import re


class HtmlReader:
    @staticmethod
    def get_simple_title(html):
        title_index = html.find("<title>")
        start_index = title_index + len("<title>")
        end_index = html.find("</title>")
        title = html[start_index:end_index]
        return title

    @staticmethod
    def get_title(test_html):
        pattern = "<title.*?>.*?</title.*?>"
        match_results = re.search(pattern, test_html, re.IGNORECASE)
        title = match_results.group()
        # Remove HTML tags
        title = re.sub("<.*?>", "", title)
        return title
