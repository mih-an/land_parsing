import re

from bs4 import BeautifulSoup


class Ads:
    square = 0
    title = ''
    price = 0
    vri = ''
    link = ''
    id = ''
    kp = ''
    address1 = ''
    address2 = ''
    address3 = ''
    address = ''
    description = ''


class CianParser:
    cian_ads_per_page = 28
    ads_card_component = 'CardComponent'
    float_pattern = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
    int_pattern = '\D'
    title_separator = ','
    link_separator = '/'

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

    def search_float_number(self, search_str):
        if re.search(self.float_pattern, search_str) is not None:
            for catch in re.finditer(self.float_pattern, search_str):
                result_float_number = float(catch[0])
                return result_float_number
        return 0

    def search_int_number(self, search_str):
        search_res = re.sub(self.int_pattern, "", search_str)
        if search_res == '':
            return 0
        return int(search_res)

    def parce_ads(self, raw_ads):
        ads = Ads()

        print(f'tag 1 = {raw_ads.name}, class = {raw_ads["class"]}, data-name={raw_ads["data-name"]}')

        target_div = raw_ads.div.a.next_sibling
        print(f'tag 2 = {target_div.name}, class = {target_div["class"]}')

        target_link = target_div.find_next('a')
        print(f'tag 3 = {target_link.name}, class = {target_link["class"]}, href = {target_link["href"]}')

        ads.link = target_link["href"]

        title_span = target_link.next_sibling.a.span.span
        print(title_span.text)

        ads.title = title_span.text
        ads.square = self.search_float_number(ads.title)

        price_span = target_link.next_sibling.next_sibling.next_sibling.next_sibling.div.span.span
        print(price_span.text)

        ads.price = self.search_int_number(price_span.text)

        p = target_link.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find_next('p')

        ads.description = p.text
        address1 = target_link.next_sibling.next_sibling.next_sibling.div.next_sibling.a
        print(address1.text)
        ads.address1 = address1.text
        address2 = address1.next_sibling.next_sibling
        print(address2.text)
        ads.address2 = address2.text
        address3 = address2.next_sibling.next_sibling
        print(address3.text)
        ads.address3 = address3.text
        ads.address = f'{ads.address1}, {ads.address2}, {ads.address3}'
        ads.kp = ads.address3

        title_parts = ads.title.split(self.title_separator)
        ads.vri = title_parts[len(title_parts) - 1].strip()

        link_parts = ads.link.split(self.link_separator)
        # - 2 because the last element is an empty element
        ads.id = link_parts[len(link_parts) - 2]

        return ads

    def get_raw_ads(self, html):
        soup = BeautifulSoup(html, "lxml")
        raw_ads_list = soup.find_all(self.is_ads_element)
        return raw_ads_list

    def get_ads(self, html):
        raw_ads_list = self.get_raw_ads(html)

        ads_list = []
        for i in range(len(raw_ads_list)):
            raw_ads = raw_ads_list[i]
            ads = Ads()
            if i == 0:
                ads = self.parce_ads(raw_ads)
            ads_list.append(ads)

        return ads_list

    def is_general_info(self, tag):
        return tag.name == 'span' and tag['data-mark'] == 'OfferTitle'

    def is_ads_element(self, tag):
        return tag.name == 'article' and tag['data-name'] == self.ads_card_component
