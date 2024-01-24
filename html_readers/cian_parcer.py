from bs4 import BeautifulSoup


class CianParser:

    @staticmethod
    def is_pagination_element(tag):
        return tag.name == 'nav' and tag['data-name'] == 'Pagination'

    def get_pages_count(self, html_text):
        soup = BeautifulSoup(html_text, "lxml")
        pagination = soup.find_all(self.is_pagination_element)
        if len(pagination) > 0 and not pagination[0].ul is None:
            pagination_tag = pagination[0]
            pages_list = pagination_tag.ul.contents
            return len(pages_list)
        else:
            return 0

    def get_page_link(self, sector_base_link: str, page_number: int):
        return ""
