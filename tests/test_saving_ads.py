import time
import unittest
import uuid
from datetime import datetime
from db.ads_database import AdsDataBase
from html_readers.cian_parcer import Ads


class TestSavingAds(unittest.TestCase):
    def test_save_ads(self):
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.create_test_ads1(ads1_uuid)
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.create_test_ads2(ads2_uuid)
        ads_list = [ads1, ads2]

        ads_db = AdsDataBase()
        ads_db.save(ads_list)

        ads_from_db = ads_db.get_ads_by_id(ads2_uuid)
        self.check_ads_are_equal(ads2, ads_from_db)
        ads_from_db = ads_db.get_ads_by_id(ads1_uuid)
        self.check_ads_are_equal(ads1, ads_from_db)

        ads_from_db = ads_db.get_ads_by_id('unknown_id')
        self.assertIsNone(ads_from_db)

    def check_ads_are_equal(self, ads2, ads_from_db):
        self.assertIsNotNone(ads_from_db)
        self.assertEqual(ads_from_db.id, ads2.id, 'Id is not correct')
        self.assertEqual(ads_from_db.title, ads2.title, 'Title is not correct')
        self.assertEqual(ads_from_db.square, ads2.square, 'Square is not correct')
        self.assertEqual(ads_from_db.price, ads2.price, 'price is not correct')
        self.assertEqual(ads_from_db.vri, ads2.vri, 'vri is not correct')
        self.assertEqual(ads_from_db.link, ads2.link, 'link is not correct')
        self.assertEqual(ads_from_db.locality, ads2.locality, 'locality is not correct')
        self.assertEqual(ads_from_db.kp, ads2.kp, 'kp is not correct')
        self.assertEqual(ads_from_db.address, ads2.address, 'address is not correct')
        self.assertEqual(ads_from_db.description, ads2.description, 'description is not correct')
        self.assertEqual(ads_from_db.kadastr_list[0], ads2.kadastr_list[0], 'Kadastr is not correct')
        self.assertEqual(ads_from_db.ads_owner, ads2.ads_owner, 'ads_owner is not correct')
        self.assertEqual(ads_from_db.ads_owner_id, ads2.ads_owner_id, 'ads_owner_id is not correct')
        self.assertEqual(ads_from_db.parce_datetime, ads2.parce_datetime, 'parce_datetime is not correct')
        self.assertEqual(ads_from_db.sector_number, ads2.sector_number, 'sector_number is not correct')

    @staticmethod
    def create_test_ads2(ads2_uuid):
        ads2 = Ads()
        ads2.title = 'Участок, 6 сот.'
        ads2.square = 6
        ads2.price = 425000
        ads2.vri = ''
        ads2.link = 'https://istra.cian.ru/sale/suburban/287210218/'
        ads2.id = ads2_uuid
        ads2.locality = 'д. Малое Ушаково'
        ads2.kp = 'КП «‎Прилесные дачи »'
        ads2.address = 'Московская область, Истра городской округ, д. Малое Ушаково'
        ads2.description = 'Самое крутое объявление 2'
        ads2.kadastr_list = ['50:08:0040229:85']
        ads2.ads_owner = 'Риелтор'
        ads2.ads_owner_id = 'ID 23674176'
        ads2.parce_datetime = datetime.now().replace(microsecond=0)
        ads2.sector_number = 2
        return ads2

    @staticmethod
    def create_test_ads1(ads1_uuid):
        ads1 = Ads()
        ads1.title = 'Участок, 9.9 сот., Садоводство'
        ads1.square = 9.9
        ads1.price = 1800000
        ads1.vri = 'Садоводство'
        ads1.link = 'https://istra.cian.ru/sale/suburban/281048577/'
        ads1.id = ads1_uuid
        ads1.locality = 'Майские Дачи кп'
        ads1.kp = 'Майские дачи 2'
        ads1.address = 'Московская область, Истра городской округ, Майские Дачи кп'
        ads1.description = 'Самое крутое объявление'
        ads1.kadastr_list = ['50:08:0040229:1139', '50:08:0040229:1165']
        ads1.electronic_trading = 'Электронные торги'
        ads1.is_electronic_trading = True
        ads1.ads_owner = 'Собственник'
        ads1.ads_owner_id = 'ID 70642111'
        ads1.parce_datetime = datetime.now().replace(microsecond=0)
        ads1.sector_number = 1
        return ads1

    def test_empty_kadastr(self):
        ads = Ads()
        ads_uuid = str(uuid.uuid4())
        ads.id = ads_uuid
        ads.title = 'Тестовый заголовок'
        ads.square = 19.9
        ads.price = 1800000
        ads.link = 'https://istra.cian.ru/sale/suburban/281048577/'
        ads.kadastr_list = []
        ads.parce_datetime = datetime.now().replace(microsecond=0)
        ads.sector_number = 1

        ads_db = AdsDataBase()
        ads_db.save([ads])

        ads_from_db = ads_db.get_ads_by_id(ads_uuid)
        self.assertIsNotNone(ads_from_db)
        self.assertEqual(ads_from_db.id, ads_uuid)
        self.assertEqual(0, len(ads_from_db.kadastr_list))

    def test_save_new_parce_iteration(self):
        # Что если спарсили тоже самое объявление второй раз или даже несколько
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.create_test_ads1(ads1_uuid)
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.create_test_ads2(ads2_uuid)
        ads_list = [ads1, ads2]
        ads_db = AdsDataBase()
        ads_db.save(ads_list)

        ads3_uuid = str(uuid.uuid4())
        new_ads3 = self.create_test_ads1(ads3_uuid)
        ads_list = [ads1, ads2, new_ads3]
        ads_db.save(ads_list)

        ads_from_db = ads_db.get_ads_by_id(ads2_uuid)
        self.check_ads_are_equal(ads2, ads_from_db)
        ads_from_db = ads_db.get_ads_by_id(ads1_uuid)
        self.check_ads_are_equal(ads1, ads_from_db)
        ads_from_db = ads_db.get_ads_by_id(ads3_uuid)
        self.check_ads_are_equal(new_ads3, ads_from_db)


    def test_ads_is_disabled(self):
        # Что если объявления уже сняли с публикации - как это важное событие отметить
        pass

    def test_save_new_price(self):
        # Что если изменилась цена - нужно это отдельно сохранять и грузить историю цен
        pass


if __name__ == '__main__':
    unittest.main()
