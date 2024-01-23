import unittest
from html_readers.regexp_reader import HtmlReader


class TestCaseGettingHtmlData(unittest.TestCase):

    def test_getting_links(self):
        with open('test_data/test_links.html', 'r') as test_html_file:
            test_html = test_html_file.read()
        links = HtmlReader().get_links(test_html)
        self.assertEqual(
            ['http://olympus.realpython.org/profiles/aphrodite',
             'http://olympus.realpython.org/profiles/poseidon',
             'http://olympus.realpython.org/profiles/dionysus'], links)


if __name__ == '__main__':
    unittest.main()
