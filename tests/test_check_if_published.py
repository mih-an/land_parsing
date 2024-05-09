import unittest
import uuid
from datetime import timedelta, datetime

from db.ads_database import AdsDataBase
from html_readers.cian_parser import CianParser
from loaders.ads_checker import AdsChecker
from tests.test_helper import TestHelper


class TestCaseAdsIsPublished(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

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

    def test_checking_unpublished(self):
        # Проверяем реально ли проходит проверка на реальном объявлении
        # https://www.cian.ru/sale/suburban/291001135/ - моё же старое объявление
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads1.link = 'https://www.cian.ru/sale/suburban/291001135/'
        # need to age ads because we don't check fresh ads
        ads1.last_parse_datetime = ads1.last_parse_datetime - timedelta(days=2)
        ads_list = [ads1]
        ads_db = AdsDataBase()
        ads_db.save(ads_list)
        self.assertFalse(ads1.is_unpublished, 'Ads should be published right after parsing')

        ads_checker = AdsChecker()
        is_unpublished = ads_checker.check_ads(ads1)
        self.assertTrue(is_unpublished, 'Ads should be unpublished because it really is')

        ads1 = ads_db.select_ads_by_id(ads1_uuid)
        self.assertTrue(ads1.is_unpublished, 'Ads should be unpublished in database also')
        delta = datetime.now() - ads1.last_parse_datetime
        self.assertEqual(0, delta.days, "Last parse datetime should be updated")

    def test_saving_published_status(self):
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads1.link = 'https://www.cian.ru/sale/suburban/291001135/'
        ads_list = [ads1]
        ads_db = AdsDataBase()
        ads_db.save(ads_list)
        self.assertFalse(ads1.is_unpublished, 'Ads should be published right after parsing')

        ads1.is_unpublished = True
        ads_db.save_published_status(ads1)
        ads1 = ads_db.select_ads_by_id(ads1_uuid)
        self.assertEqual(ads1.is_unpublished, True, 'Ads should be unpublished in database')

        ads1.is_unpublished = False
        ads_db.save_published_status(ads1)
        ads1 = ads_db.select_ads_by_id(ads1_uuid)
        self.assertEqual(ads1.is_unpublished, False, 'Ads should be published in database now')

    def test_published_again_after_parsing(self):
        # new published ads
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads_list = [ads1]
        ads_db = AdsDataBase()
        ads_db.save(ads_list)

        # let's assume we've checked ads and it's unpublished already
        ads1.is_unpublished = True
        ads_db.save_published_status(ads1)
        ads1 = ads_db.select_ads_by_id(ads1_uuid)
        self.assertEqual(ads1.is_unpublished, True, 'Ads should be unpublished in database now')

        # let's assume we parse it again, and it's again in the parsing list, and we saved it to database
        ads1.is_unpublished = False
        ads_list = [ads1]
        ads_db.save(ads_list)

        # Now we expect that ads should be published again in database
        ads1 = ads_db.select_ads_by_id(ads1_uuid)
        self.assertEqual(ads1.is_unpublished, False, 'Ads should be published in database after parsing')


if __name__ == '__main__':
    unittest.main()
