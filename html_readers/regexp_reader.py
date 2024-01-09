import re
from bs4 import BeautifulSoup


class HtmlReader:
    @staticmethod
    def get_title(html_text):
        pattern = "<title.*?>.*?</title.*?>"
        match_results = re.search(pattern, html_text, re.IGNORECASE)
        title = match_results.group()
        # Remove HTML tags
        title = re.sub("<.*?>", "", title)
        return title

    @staticmethod
    def get_name(html_text):
        return HtmlReader.get_item(html_text, "Name: ")

    @staticmethod
    def get_fav_color(html_text):
        return HtmlReader.get_item(html_text, "Favorite Color:")

    @staticmethod
    def get_item(html_text, search_text):
        string_start_idx = html_text.find(search_text)
        text_start_idx = string_start_idx + len(search_text)

        next_html_tag_offset = html_text[text_start_idx:].find("<")
        text_end_idx = text_start_idx + next_html_tag_offset

        raw_text = html_text[text_start_idx: text_end_idx]
        clean_text = raw_text.strip(" \r\n\t")
        return clean_text

    @staticmethod
    def get_links(html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        links_tag = soup.find_all("a")

        link_lst = []
        for link in links_tag:
            link_lst.append("http://olympus.realpython.org" + link["href"])

        return link_lst
