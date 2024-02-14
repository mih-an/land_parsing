import unittest
import uuid

from db.ads_database import AdsDataBase
from html_readers.cian_parcer import Ads


class TestSavingAds(unittest.TestCase):
    def test_save_ads(self):
        ads1 = Ads()
        ads1.title = 'Участок, 9.9 сот., Садоводство'
        ads1.square = 9.9
        ads1.price = 1800000
        ads1.vri = 'Садоводство'
        ads1.link = 'https://istra.cian.ru/sale/suburban/281048577/'
        ads1_uuid = str(uuid.uuid4())
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

        ads2 = Ads()
        ads2.title = 'Участок, 6 сот.'
        ads2.square = 6
        ads2.price = 425000
        ads2.vri = ''
        ads2.link = 'https://istra.cian.ru/sale/suburban/287210218/'
        ads2_uuid = str(uuid.uuid4())
        ads2.id = ads2_uuid
        ads2.locality = 'д. Малое Ушаково'
        ads2.kp = 'КП «‎Прилесные дачи »'
        ads2.address = 'Московская область, Истра городской округ, д. Малое Ушаково'
        ads2.description = 'Самое крутое объявление 2'
        ads2.kadastr_list = ['50:08:0040229:85']
        ads2.ads_owner = 'Риелтор'
        ads2.ads_owner_id = 'ID 23674176'

        ads_list = [ads1, ads2]

        ads_db = AdsDataBase()
        ads_db.save(ads_list)

        ads_from_db = ads_db.get_ads_by_id(ads2_uuid)
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

        ads_from_db = ads_db.get_ads_by_id(ads1_uuid)
        self.assertIsNotNone(ads_from_db)
        self.assertEqual(ads_from_db.id, ads1.id)
        self.assertEqual(ads_from_db.title, ads1.title)
        self.assertEqual(ads_from_db.square, ads1.square)
        self.assertEqual(ads_from_db.price, ads1.price)
        self.assertEqual(ads_from_db.vri, ads1.vri)
        self.assertEqual(ads_from_db.link, ads1.link)
        self.assertEqual(ads_from_db.locality, ads1.locality)
        self.assertEqual(ads_from_db.kp, ads1.kp)
        self.assertEqual(ads_from_db.address, ads1.address)
        self.assertEqual(ads_from_db.description, ads1.description)
        self.assertEqual(ads_from_db.kadastr_list[0], ads1.kadastr_list[0])
        self.assertEqual(ads_from_db.ads_owner, ads1.ads_owner)
        self.assertEqual(ads_from_db.ads_owner_id, ads1.ads_owner_id)

        ads_from_db = ads_db.get_ads_by_id('unknown_id')
        self.assertIsNone(ads_from_db)

    def test_empty_kadastr(self):
        ads = Ads()
        ads_uuid = str(uuid.uuid4())
        ads.id = ads_uuid
        ads.title = 'Тестовый заголовок'
        ads.square = 19.9
        ads.price = 1800000
        ads.link = 'https://istra.cian.ru/sale/suburban/281048577/'
        ads.kadastr_list = []

        ads_db = AdsDataBase()
        ads_db.save([ads])

        ads_from_db = ads_db.get_ads_by_id(ads_uuid)
        self.assertIsNotNone(ads_from_db)
        self.assertEqual(ads_from_db.id, ads_uuid)
        self.assertEqual(0, len(ads_from_db.kadastr_list))

    def test_save_new_price(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
