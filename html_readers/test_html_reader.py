import unittest

from html_readers.regexp_reader import HtmlReader


class TestCaseGettingHtmlData(unittest.TestCase):
    def test_getting_html_title(self):
        with open('test_data/test_html.html', 'r') as test_html_file:
            test_html = test_html_file.read()
        html_title = HtmlReader().get_title(test_html)
        self.assertEqual("Profile: Dionysus", html_title)

    def test_getting_name(self):
        with open('test_data/test_html.html', 'r') as test_html_file:
            test_html = test_html_file.read()
        name = HtmlReader().get_name(test_html)
        self.assertEqual("Dionysus", name)

    def test_getting_favorite_color(self):
        with open('test_data/test_html.html', 'r') as test_html_file:
            test_html = test_html_file.read()
        fav_color = HtmlReader().get_fav_color(test_html)
        self.assertEqual("Wine", fav_color)

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
