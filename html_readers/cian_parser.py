import re

from bs4 import BeautifulSoup
from html_readers.ads import Ads
from html_readers.parse_helper import ParseHelper


class CianParser:

    def __init__(self):
        self.offer_subtitle_data_mark = 'OfferSubtitle'
        self.electronic_data_name = 'GalleryLabels'
        self.agency = 'Агентство недвижимости'
        self.brand_area_data_name = 'BrandingLevelWrapper'
        self.kp_data_name = 'ContentRow'
        self.offer_title_data_mark = 'OfferTitle'
        self.price_span_data_mark = 'MainPrice'
        self.address_data_name = 'GeoLabel'
        self.link_area_data_name = 'LinkArea'
        self.description_data_name = 'Description'
        self.ads_card_component = 'CardComponent'
        self.substr = "offer_type=suburban"
        self.parse_helper = ParseHelper()
        self.cian_ads_per_page = 28
        self.title_separator = ','
        self.address_separator = ', '
        self.link_separator = '/'
        self.vri_dict = {'Садоводство', 'ИЖС', 'ДНП', 'ЛПХ', 'Личное подсобное хозяйство', 'Фермерское хозяйство'}

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

    @staticmethod
    def parse_link(target_div):
        target_link = target_div.find_next('a')
        return target_link["href"]

    def parse_ads(self, raw_ads):
        ads = Ads()
        target_div = raw_ads.find_next(self.is_main_link_area_tag)

        ads.link = self.parse_link(target_div)
        ads.title = self.parse_title(target_div)
        ads.square = self.parse_square(ads.title)
        ads.price = self.parse_price(target_div)
        self.parse_address(ads, target_div)
        ads.description = self.parse_description(target_div)
        ads.vri = self.get_vri(ads.title)
        ads.id = self.parse_id(ads)
        ads.kp = self.parse_kp(target_div)
        self.parse_owner(ads, raw_ads)
        self.parse_electronic_trading(ads, raw_ads)
        self.parse_kadastr_number(ads)

        return ads

    def get_raw_ads(self, html):
        soup = BeautifulSoup(html, "lxml")
        raw_ads_list = soup.find_all(self.is_ads_tag)
        return raw_ads_list

    def get_ads(self, html):
        raw_ads_list = self.get_raw_ads(html)

        ads_list = []
        for raw_ads in raw_ads_list:
            ads = self.parse_ads(raw_ads)
            ads_list.append(ads)

        return ads_list

    @staticmethod
    def is_needed_tag(tag, tag_name, data_attr_key, data_attr_value):
        return tag.name == tag_name and data_attr_key in tag.attrs.keys() and tag[data_attr_key] == data_attr_value

    def is_ads_tag(self, tag):
        return self.is_needed_tag(tag, 'article', 'data-name', self.ads_card_component)

    def is_brand_main_tag(self, tag):
        return self.is_needed_tag(tag, 'div', 'data-name', self.brand_area_data_name)

    def is_electronic_tag(self, tag):
        return self.is_needed_tag(tag, 'div', 'data-name', self.electronic_data_name)

    def is_main_link_area_tag(self, tag):
        return self.is_needed_tag(tag, 'div', 'data-name', self.link_area_data_name)

    def is_description_tag(self, tag):
        return self.is_needed_tag(tag, 'div', 'data-name', self.description_data_name)

    def is_offer_title_tag(self, tag):
        return self.is_needed_tag(tag, 'span', 'data-mark', self.offer_title_data_mark)

    def is_offer_subtitle_tag(self, tag):
        return self.is_needed_tag(tag, 'span', 'data-mark', self.offer_subtitle_data_mark)

    def is_price_tag(self, tag):
        return self.is_needed_tag(tag, 'span', 'data-mark', self.price_span_data_mark)

    def is_address_tag(self, tag):
        return (self.is_needed_tag(tag, 'a', 'data-name', self.address_data_name) or
                self.is_needed_tag(tag, 'span', 'data-name', self.address_data_name))

    def is_kp_tag(self, tag):
        return self.is_needed_tag(tag, 'div', 'data-name', self.kp_data_name)

    def get_vri(self, title):
        title_parts = title.split(self.title_separator)
        vri = title_parts[len(title_parts) - 1].strip()
        if vri not in self.vri_dict:
            vri = ''
        return vri

    def parse_title(self, target_div):
        subtitle = self.parse_subtitle(target_div)
        if subtitle == '':
            title = target_div.find_next(self.is_offer_title_tag).span.text
        else:
            title = subtitle

        return title

    def parse_subtitle(self, target_div):
        subtitle = ''
        offer_title_tag = target_div.find_next(self.is_offer_title_tag)
        next_sibling = offer_title_tag.next_sibling
        if next_sibling is not None and next_sibling.span is not None:
            subtitle_tag = next_sibling.span
            if self.is_offer_subtitle_tag(subtitle_tag):
                subtitle = subtitle_tag.text
        return subtitle

    def parse_price(self, target_div):
        price_span = target_div.find_next(self.is_price_tag).span
        price = self.parse_helper.search_int_number(price_span.text)
        return price

    def parse_address(self, ads, target_div):
        address_first_tag = target_div.find_next(self.is_address_tag)

        address_div_tag = address_first_tag.parent
        address_list = []
        for tag in address_div_tag.contents:
            if self.is_address_tag(tag):
                address_list.append(tag.text)

        ads.address = self.address_separator.join(address_list)

    def parse_description(self, target_div):
        p = target_div.find_next(self.is_description_tag).p
        return p.text

    def parse_id(self, ads):
        link_parts = ads.link.split(self.link_separator)
        # - 2 because the last element is an empty element
        ads_id = link_parts[len(link_parts) - 2]
        return ads_id

    def parse_kp(self, target_div):
        price_span = target_div.find_next(self.is_price_tag)
        kp_parent_div_tag = price_span.parent.parent.next_sibling
        kp_tag = kp_parent_div_tag.find_next(self.is_kp_tag)
        if kp_tag is not None and kp_tag.a is not None:
            return kp_tag.a.text

        return ''

    def parse_owner(self, ads, raw_ads):
        brand_div = raw_ads.find_next(self.is_brand_main_tag)
        span = brand_div.div.div.next_sibling.div.div.span
        ads.ads_owner = span.text

        next_sib = span.next_sibling
        if ads.ads_owner == self.agency and next_sib.a is not None:
            owner_id = next_sib.a.span.text
        else:
            owner_id = next_sib.span.text

        ads.ads_owner_id = owner_id

    def parse_electronic_trading(self, ads, raw_ads):
        electronic_tag = raw_ads.div.a.div.next_sibling
        if electronic_tag is not None and self.is_electronic_tag(electronic_tag):
            ads.electronic_trading = electronic_tag.div.text
            ads.is_electronic_trading = True

    def parse_kadastr_number(self, ads):
        ads.kadastr_list = self.parse_helper.parse_kadastr(ads.description)

    def parse_square(self, title):
        return self.parse_helper.parse_square(title)
