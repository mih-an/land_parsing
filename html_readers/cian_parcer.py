import re

from bs4 import BeautifulSoup


class CianParser:
    cian_ads_per_page = 28
    ads_card_component = 'CardComponent'

    def __init__(self):
        self.substr = "offer_type=suburban"

    def get_pages_count(self, html_text):
        soup = BeautifulSoup(html_text, "lxml")
        if soup.title is None or soup.title.text == '':
            return 1

        search_result = re.search(r'\d+', soup.title.text)
        if search_result is None:
            return 1

        ads_count = int(search_result.group())
        pages_count = ads_count // self.cian_ads_per_page
        return pages_count + 1

    def get_page_link(self, sector_base_link: str, page_number: int):
        # Looking for substring "offer_type=suburban"
        page_substr_pos = sector_base_link.find(self.substr) + len(self.substr)
        # Inserting page number
        page_link = sector_base_link[:page_substr_pos] + f"&p={page_number}" + sector_base_link[page_substr_pos:]

        return page_link

    def get_ads(self, html):
        soup = BeautifulSoup(html, "lxml")
        ads_list = soup.find_all(self.is_ads_element)
        return ads_list

    def is_ads_element(self, tag):
        return tag.name == 'article' and tag['data-name'] == self.ads_card_component
