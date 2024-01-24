from bs4 import BeautifulSoup


class CianParser:

    def __init__(self):
        self.substr = "offer_type=suburban"

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
        # Looking for substring "offer_type=suburban"
        substr_pos = sector_base_link.find(self.substr) + len(self.substr)
        print("-"*100)
        print(substr_pos)
        print("-" * 100)
        print(sector_base_link[:substr_pos])
        print("-" * 100)
        print(sector_base_link[substr_pos:])
        # Inserting page number
        page_link = sector_base_link[:substr_pos] + f"&p={page_number}" + sector_base_link[substr_pos:]
        print(page_link)

        return page_link
