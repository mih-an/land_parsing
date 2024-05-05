import time
import unittest
import uuid
from datetime import datetime
from db.ads_database import AdsDataBase
from html_readers.cian_parser import Ads
from tests.test_helper import TestHelper


class TestSavingAds(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_save_ads(self):
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.test_helper.create_test_ads2(ads2_uuid)
        ads_list = [ads1, ads2]

        ads_db = AdsDataBase()
        ads_db.save(ads_list)

        ads_from_db = ads_db.select_ads_by_id(ads2_uuid)
        self.check_ads_are_equal(ads2, ads_from_db)
        ads_from_db = ads_db.select_ads_by_id(ads1_uuid)
        self.check_ads_are_equal(ads1, ads_from_db)

        ads_from_db = ads_db.select_ads_by_id('unknown_id')
        self.assertIsNone(ads_from_db)

    def check_ads_are_equal(self, ads2, ads_from_db):
        self.test_helper.check_ads_are_equal(ads2, ads_from_db)

    def test_empty_kadastr(self):
        ads = Ads()
        ads_uuid = str(uuid.uuid4())
        ads.id = ads_uuid
        ads.title = 'Тестовый заголовок'
        ads.square = 19.9
        ads.price = 1800000
        ads.link = 'https://istra.cian.ru/sale/suburban/281048577/'
        ads.kadastr_list = []
        ads.first_parse_datetime = datetime.now().replace(microsecond=0)
        ads.last_parse_datetime = ads.first_parse_datetime
        ads.sector_number = 1

        ads_db = AdsDataBase()
        ads_db.save([ads])

        ads_from_db = ads_db.select_ads_by_id(ads_uuid)
        self.assertIsNotNone(ads_from_db)
        self.assertEqual(ads_from_db.id, ads_uuid)
        self.assertEqual(0, len(ads_from_db.kadastr_list))

    def test_save_new_parce_iteration(self):
        # Test when we parce the same ads second time and also parce new ads
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.test_helper.create_test_ads2(ads2_uuid)
        ads_list = [ads1, ads2]
        ads_db = AdsDataBase()
        ads_db.save(ads_list)

        ads3_uuid = str(uuid.uuid4())
        new_ads3 = self.test_helper.create_test_ads1(ads3_uuid)
        ads_list = [ads1, ads2, new_ads3]
        ads_db.save(ads_list)

        ads_from_db = ads_db.select_ads_by_id(ads2_uuid)
        self.check_ads_are_equal(ads2, ads_from_db)
        ads_from_db = ads_db.select_ads_by_id(ads1_uuid)
        self.check_ads_are_equal(ads1, ads_from_db)
        ads_from_db = ads_db.select_ads_by_id(ads3_uuid)
        self.check_ads_are_equal(new_ads3, ads_from_db)

    def test_save_new_price(self):
        # Test that new price is correctly saved
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.test_helper.create_test_ads2(ads2_uuid)
        ads_list = [ads1, ads2]
        ads_db = AdsDataBase()
        ads_db.save(ads_list)

        ads1.price = 3000000
        second_price_datetime = datetime.now().replace(microsecond=0)
        ads1.last_parse_datetime = second_price_datetime
        ads_list = [ads1, ads2]
        ads_db.save(ads_list)

        ads_from_db = ads_db.select_ads_by_id(ads1_uuid)
        self.check_ads_are_equal(ads1, ads_from_db)
        ads_from_db = ads_db.select_ads_by_id(ads2_uuid)
        self.check_ads_are_equal(ads2, ads_from_db)

    def test_price_history(self):
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        first_price_date_time = ads1.first_parse_datetime
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.test_helper.create_test_ads2(ads2_uuid)
        ads_list = [ads1, ads2]
        ads_db = AdsDataBase()
        ads_db.save(ads_list)

        ads1.price = 3000000
        second_price_datetime = datetime.now().replace(microsecond=0)
        ads1.first_parse_datetime = second_price_datetime
        ads_list = [ads1, ads2]
        ads_db.save(ads_list)

        price_history = ads_db.select_price_history(ads1_uuid)
        self.assertIsNotNone(price_history)
        self.assertEqual(2, len(price_history))
        self.assertEqual(1800000, price_history[0].price)
        self.assertEqual(first_price_date_time, price_history[0].price_datetime)
        self.assertEqual(3000000, price_history[1].price)
        self.assertEqual(second_price_datetime, price_history[1].price_datetime)

    def test_last_parce_time_updated(self):
        # To separate "disabled ads" from "still alive" we need to store last parsing time.
        # "Disabled" ads will be ads that has last_parse_time less than other at the same sector

        # First time parce ads and save it to database
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads_db = AdsDataBase()
        ads_list = [ads1]
        ads_db.save(ads_list)

        # Check if last_parce_datetime equals parce_date_time for the first saving
        ads_from_db = ads_db.select_ads_by_id(ads1_uuid)
        self.assertEqual(ads1.first_parse_datetime, ads_from_db.last_parse_datetime,
                         'Last_parce_time should be equal parce_time for the first time')

        # Let's pretend that we parce the same ads second time
        # Nothing has changed except parsing time. Even price hasn't changed
        # Need to sleep for a moment, otherwise, time could be the same, because we don't count milliseconds
        time.sleep(1)
        ads1.last_parse_datetime = datetime.now().replace(microsecond=0)
        ads_list = [ads1]
        ads_db.save(ads_list)

        # Information about last parsing time should be updated
        ads_from_db = ads_db.select_ads_by_id(ads1_uuid)
        self.check_ads_are_equal(ads1, ads_from_db)
        self.assertEqual(ads1.last_parse_datetime, ads_from_db.last_parse_datetime)
        self.assertNotEqual(ads1.last_parse_datetime, ads_from_db.first_parse_datetime)
        self.assertNotEqual(ads_from_db.last_parse_datetime, ads_from_db.first_parse_datetime)


if __name__ == '__main__':
    unittest.main()
