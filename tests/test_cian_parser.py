import unittest

from html_readers.cian_parcer import CianParser


class TestCianParser(unittest.TestCase):
    def test_pages_count(self):
        with open('cian_pages/cian_sector_21_p1.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        pages_count = cian_parser.get_pages_count(test_html)

        self.assertEqual(5, pages_count, "Wrong pages count:")  # add assertion here

    def test_no_pagination(self):
        with open('cian_pages/cian_sector1.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        pages_count = cian_parser.get_pages_count(test_html)
        self.assertEqual(0, pages_count)

    def test_pages_links(self):
        # Getting sector link
        # Getting pages count
        # Creating all necessary links from base link and pages count

        # Checkin all links
        self.assertEqual(True, False)

    def test_no_pagination_pages_links(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
