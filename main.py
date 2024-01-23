
from bs4 import BeautifulSoup


def is_pagination_element(tag):
    return tag.name == 'nav' and tag['data-name'] == 'Pagination'


with open('tests/cian_pages/cian_sector_21_p1.html', 'r') as test_html_file:
    test_html = test_html_file.read()

soup = BeautifulSoup(test_html, "lxml")
nav_list = soup.find_all(is_pagination_element)

for child in nav_list[0].ul.children:
    print(child)



