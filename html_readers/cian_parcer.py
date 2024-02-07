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
    locality = ''
    address1 = ''
    address2 = ''
    address3 = ''
    address = ''
    description = ''


class CianParser:
    cian_ads_per_page = 28
    float_pattern = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
    int_pattern = '\D'
    title_separator = ','
    link_separator = '/'
    vri_dict = {'Садоводство', 'ИЖС', 'ДНП', 'ЛПХ', 'Личное подсобное хозяйство', 'Фермерское хозяйство'}

    def __init__(self):
        self.kp_data_name = 'ContentRow'
        self.offer_title_data_mark = 'OfferTitle'
        self.price_span_data_mark = 'MainPrice'
        self.address_data_name = 'GeoLabel'
        self.link_area_data_name = 'LinkArea'
        self.description_data_name = 'Description'
        self.ads_card_component = 'CardComponent'
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

    @staticmethod
    def parce_link(target_div):
        target_link = target_div.find_next('a')
        print(f'Link: {target_link["href"]}')
        return target_link["href"]

    def parce_ads(self, raw_ads):
        ads = Ads()
        print(f'Ads div = {raw_ads.name}, class = {raw_ads["class"]}, data-name={raw_ads["data-name"]}')

        target_div = raw_ads.find_next(self.is_main_link_area_tag)
        print(f'Target div = {target_div.name}, class = {target_div["class"]}')

        ads.link = self.parce_link(target_div)
        ads.title = self.parce_title(target_div)
        ads.square = self.search_float_number(ads.title)
        print(f'Square: {ads.square}')
        ads.price = self.parce_price(target_div)
        self.parce_address(ads, target_div)
        ads.description = self.parce_description(target_div)
        ads.vri = self.get_vri(ads.title)
        ads.id = self.parce_id(ads)
        ads.kp = self.parce_kp(target_div)

        return ads

    def get_raw_ads(self, html):
        soup = BeautifulSoup(html, "lxml")
        raw_ads_list = soup.find_all(self.is_ads_tag)
        return raw_ads_list

    def get_ads(self, html):
        raw_ads_list = self.get_raw_ads(html)

        ads_list = []
        for i in range(len(raw_ads_list)):
            print('-' * 50)
            print(f'ads number = {i}')
            raw_ads = raw_ads_list[i]
            ads = self.parce_ads(raw_ads)
            ads_list.append(ads)

        return ads_list

    @staticmethod
    def is_needed_tag(tag, tag_name, data_attr_key, data_attr_value):
        return tag.name == tag_name and data_attr_key in tag.attrs.keys() and tag[data_attr_key] == data_attr_value

    def is_ads_tag(self, tag):
        return self.is_needed_tag(tag, 'article', 'data-name', self.ads_card_component)

    def is_main_link_area_tag(self, tag):
        return self.is_needed_tag(tag, 'div', 'data-name', self.link_area_data_name)

    def is_description_tag(self, tag):
        return self.is_needed_tag(tag, 'div', 'data-name', self.description_data_name)

    def is_offer_title_tag(self, tag):
        return self.is_needed_tag(tag, 'span', 'data-mark', self.offer_title_data_mark)

    def is_price_tag(self, tag):
        return self.is_needed_tag(tag, 'span', 'data-mark', self.price_span_data_mark)

    def is_address_tag(self, tag):
        return self.is_needed_tag(tag, 'a', 'data-name', self.address_data_name)

    def is_kp_tag(self, tag):
        return self.is_needed_tag(tag, 'div', 'data-name', self.kp_data_name)

    def get_vri(self, title):
        title_parts = title.split(self.title_separator)
        vri = title_parts[len(title_parts) - 1].strip()
        if vri not in self.vri_dict:
            vri = ''
        print(f'VRI: {vri}')
        return vri

    def parce_title(self, target_div):
        title_span = target_div.find_next(self.is_offer_title_tag).span
        print(f'Title: {title_span.text}')
        return title_span.text

    def parce_price(self, target_div):
        price_span = target_div.find_next(self.is_price_tag).span
        price = self.search_int_number(price_span.text)
        print(f'Price int: {price}, price str: {price_span.text}')
        return price

    def parce_address(self, ads, target_div):
        address1 = target_div.find_next(self.is_address_tag)
        ads.address1 = address1.text
        # Two times next_sibling because it has comma between a tags
        address2 = address1.next_sibling.next_sibling
        ads.address2 = address2.text
        address3 = address2.next_sibling.next_sibling
        ads.address3 = address3.text
        ads.address = f'{ads.address1}, {ads.address2}, {ads.address3}'
        ads.locality = ads.address3
        print(f'Address: {ads.address}')
        print(f'Locality: {ads.locality}')

    def parce_description(self, target_div):
        p = target_div.find_next(self.is_description_tag).p
        return p.text

    def parce_id(self, ads):
        link_parts = ads.link.split(self.link_separator)
        # - 2 because the last element is an empty element
        ads_id = link_parts[len(link_parts) - 2]
        print(f'Id: {ads_id}')
        return ads_id

    def parce_kp(self, target_div):
        price_span = target_div.find_next(self.is_price_tag)
        kp_parent_div_tag = price_span.parent.parent.next_sibling
        kp_tag = kp_parent_div_tag.find_next(self.is_kp_tag)
        if kp_tag is not None and kp_tag.a is not None:
            print(f'Cottage complex: {kp_tag.a.text}')
            return kp_tag.a.text

        return ''
