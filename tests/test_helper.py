import unittest
from datetime import datetime
from html_readers.ads import Ads


class TestHelper(unittest.TestCase):
    @staticmethod
    def create_test_ads1(ads_uuid):
        ads = Ads()
        ads.title = 'Участок, 9.9 сот., Садоводство'
        ads.square = 9.9
        ads.price = 1800000
        ads.vri = 'Садоводство'
        ads.link = 'https://istra.cian.ru/sale/suburban/281048577/'
        ads.id = ads_uuid
        ads.kp = 'Майские дачи 2'
        ads.address = 'Московская область, Истра городской округ, Майские Дачи кп'
        ads.description = 'Самое крутое объявление'
        ads.kadastr_list = ['50:08:0040229:1139', '50:08:0040229:1165']
        ads.electronic_trading = 'Электронные торги'
        ads.is_electronic_trading = True
        ads.ads_owner = 'Собственник'
        ads.ads_owner_id = 'ID 70642111'
        ads.first_parse_datetime = datetime.now().replace(microsecond=0)
        ads.last_parse_datetime = ads.first_parse_datetime
        ads.to_call_datetime = ads.first_parse_datetime
        ads.sector_number = 1
        return ads

    @staticmethod
    def create_test_ads2(ads_uuid):
        ads = Ads()
        ads.title = 'Участок, 6 сот.'
        ads.square = 6
        ads.price = 425000
        ads.vri = ''
        ads.link = 'https://istra.cian.ru/sale/suburban/287210218/'
        ads.id = ads_uuid
        ads.kp = 'КП «‎Прилесные дачи »'
        ads.address = 'Московская область, Истра городской округ, д. Малое Ушаково'
        ads.description = 'Самое крутое объявление 2'
        ads.kadastr_list = ['50:08:0040229:85']
        ads.ads_owner = 'Риелтор'
        ads.ads_owner_id = 'ID 23674176'
        ads.first_parse_datetime = datetime.now().replace(microsecond=0)
        ads.last_parse_datetime = ads.first_parse_datetime
        ads.to_call_datetime = ads.first_parse_datetime
        ads.sector_number = 2
        return ads

    def check_ads_are_equal(self, ads2, ads_from_db):
        self.assertIsNotNone(ads_from_db)
        self.assertEqual(ads_from_db.id, ads2.id, 'Id is not correct')
        self.assertEqual(ads_from_db.title, ads2.title, 'Title is not correct')
        self.assertEqual(ads_from_db.square, ads2.square, 'Square is not correct')
        self.assertEqual(ads_from_db.price, ads2.price, 'price is not correct')
        self.assertEqual(ads_from_db.vri, ads2.vri, 'vri is not correct')
        self.assertEqual(ads_from_db.link, ads2.link, 'link is not correct')
        self.assertEqual(ads_from_db.kp, ads2.kp, 'kp is not correct')
        self.assertEqual(ads_from_db.address, ads2.address, 'address is not correct')
        self.assertEqual(ads_from_db.description, ads2.description, 'description is not correct')
        self.assertEqual(ads_from_db.kadastr_list[0], ads2.kadastr_list[0], 'Kadastr is not correct')
        self.assertEqual(ads_from_db.ads_owner, ads2.ads_owner, 'ads_owner is not correct')
        self.assertEqual(ads_from_db.ads_owner_id, ads2.ads_owner_id, 'ads_owner_id is not correct')
        self.assertEqual(ads_from_db.first_parse_datetime, ads2.first_parse_datetime, 'parce_datetime is not correct')
        self.assertEqual(ads_from_db.sector_number, ads2.sector_number, 'sector_number is not correct')
