import unittest

from html_readers.regexp_reader import HtmlReader


class TestCaseGettingHtmlData(unittest.TestCase):
    def test_getting_html_title(self):
        html_reader = HtmlReader()
        with open('test_bad_title.html', 'r') as test_html_file:
            test_html = test_html_file.read()
        html_title = html_reader.get_title(test_html)
        self.assertEqual("Profile: Dionysus", html_title)


if __name__ == '__main__':
    unittest.main()
