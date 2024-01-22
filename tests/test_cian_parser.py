import unittest

from html_readers.cian_parcer import CianParcer
from loaders.html_file_loader import HtmlLoader


class TestCianParser(unittest.TestCase):
    def test_pages_count(self):
        path_to_html = "cian_data/cian_page1.html'"
        html_loader = HtmlLoader()
        html = html_loader.load_from_file(path_to_html)

        cian_parser = CianParcer()
        pages_count = cian_parser.get_pages_count(html)

        self.assertEqual(5, pages_count, "Wrong pages count:")  # add assertion here


if __name__ == '__main__':
    unittest.main()
