import unittest

from html_readers.cian_parser import CianParser


class TestCaseAdsIsPublished(unittest.TestCase):
    def test_html_ads_is_published(self):
        with open('test_data/ads_unpublished.html', 'r') as ads_html_file:
            ads_html = ads_html_file.read()
        cian_parser = CianParser()
        is_unpublished = cian_parser.is_unpublished(ads_html)
        self.assertEqual(is_unpublished, True, 'Ads should be unpublished')

        with open('test_data/ads_published.html', 'r') as ads_html_file:
            ads_html = ads_html_file.read()
        cian_parser = CianParser()
        is_unpublished = cian_parser.is_unpublished(ads_html)
        self.assertEqual(is_unpublished, False, 'Ads should be published')


if __name__ == '__main__':
    unittest.main()
