import unittest
import uuid
from datetime import datetime

from google_sheets.google_sheets_saver import GoogleSheetsWorker
from html_readers.ads import Ads


class SavingAdsToGoogleSheetsTestCase(unittest.TestCase):
    def test_save_new_ads_to_google_sheets(self):
        new_ads_url = "https://docs.google.com/spreadsheets/d/1PMfgsa1wN1eWtwCCIWOCwTH1HQpz3Jb4o746Qc8UfLw"
        sheets_id = new_ads_url[39:]
        credentials_file = '../creds/google_creds.json'

        ads1 = Ads()
        ads1.id = 'id 1'
        ads2 = Ads()
        ads2.id = 'id 2'
        ads_list = [ads1, ads2]

        gs_ads_worker = GoogleSheetsWorker()
        gs_ads_worker.save_ads(ads_list, sheets_id, credentials_file, "Values")

        ads_list_from_gs = gs_ads_worker.load_ads(sheets_id, credentials_file, "Values")
        self.assertEqual(2, len(ads_list_from_gs))
        self.assertEqual('id 1', ads_list_from_gs[0][0])
        self.assertEqual('id 2', ads_list_from_gs[1][0])

    def test_save_new_ads2(self):
        new_ads_url = "https://docs.google.com/spreadsheets/d/1PMfgsa1wN1eWtwCCIWOCwTH1HQpz3Jb4o746Qc8UfLw"
        sheets_id = new_ads_url[39:]
        credentials_file = '../creds/google_creds.json'

        ads1_uuid = str(uuid.uuid4())
        ads1 = self.create_test_ads1(ads1_uuid)
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.create_test_ads2(ads2_uuid)
        ads_list = [ads1, ads2]

        gs_ads_worker = GoogleSheetsWorker()
        gs_ads_worker.save_ads(ads_list, sheets_id, credentials_file, 'today')
        ads_list_from_gs = gs_ads_worker.load_ads(sheets_id, credentials_file, 'today')
        self.assertEqual(2, len(ads_list_from_gs))

        self.assertEqual(ads1_uuid, ads_list_from_gs[0][0])
        self.assertEqual(str(ads1.sector_number), ads_list_from_gs[0][1])
        self.assertEqual(ads1.title, ads_list_from_gs[0][2])
        self.assertEqual(str(ads1.square), ads_list_from_gs[0][3])
        self.assertEqual(str(ads1.price), ads_list_from_gs[0][4])
        self.assertEqual(ads1.vri, ads_list_from_gs[0][6])
        self.assertEqual(ads1.link, ads_list_from_gs[0][7])
        self.assertEqual(ads1.kp, ads_list_from_gs[0][8])
        self.assertEqual(ads1.address, ads_list_from_gs[0][9])
        self.assertEqual(','.join(ads1.kadastr_list), ads_list_from_gs[0][10])
        self.assertEqual(ads1.ads_owner, ads_list_from_gs[0][11])
        self.assertEqual(ads1.ads_owner_id, ads_list_from_gs[0][12])
        self.assertEqual(str(ads1.first_parse_datetime), ads_list_from_gs[0][13])
        self.assertEqual(ads1.description, ads_list_from_gs[0][14])

        self.assertEqual(ads2_uuid, ads_list_from_gs[1][0])
        self.assertEqual(str(ads2.sector_number), ads_list_from_gs[1][1])
        self.assertEqual(ads2.title, ads_list_from_gs[1][2])
        self.assertEqual(str(ads2.square), ads_list_from_gs[1][3])
        self.assertEqual(str(ads2.price), ads_list_from_gs[1][4])
        self.assertEqual(ads2.vri, ads_list_from_gs[1][6])
        self.assertEqual(ads2.link, ads_list_from_gs[1][7])
        self.assertEqual(ads2.kp, ads_list_from_gs[1][8])
        self.assertEqual(ads2.address, ads_list_from_gs[1][9])
        self.assertEqual(','.join(ads2.kadastr_list), ads_list_from_gs[1][10])
        self.assertEqual(ads2.ads_owner, ads_list_from_gs[1][11])
        self.assertEqual(ads2.ads_owner_id, ads_list_from_gs[1][12])
        self.assertEqual(str(ads2.first_parse_datetime), ads_list_from_gs[1][13])
        self.assertEqual(ads2.description, ads_list_from_gs[1][14])

    def test_adding_header(self):
        new_ads_url = "https://docs.google.com/spreadsheets/d/1PMfgsa1wN1eWtwCCIWOCwTH1HQpz3Jb4o746Qc8UfLw"
        sheets_id = new_ads_url[39:]
        credentials_file = '../creds/google_creds.json'

        ads1_uuid = str(uuid.uuid4())
        ads1 = self.create_test_ads1(ads1_uuid)
        ads_list = [ads1]

        gs_ads_worker = GoogleSheetsWorker()
        gs_ads_worker.save_ads(ads_list, sheets_id, credentials_file, "today")
        ads_list_from_gs = gs_ads_worker.load_ads_with_title(sheets_id, credentials_file, "today")
        self.assertEqual(2, len(ads_list_from_gs))

        self.assertEqual('id', ads_list_from_gs[0][0])
        self.assertEqual('sector_number', ads_list_from_gs[0][1])
        self.assertEqual('title', ads_list_from_gs[0][2])
        self.assertEqual('square', ads_list_from_gs[0][3])
        self.assertEqual('price', ads_list_from_gs[0][4])
        self.assertEqual('vri', ads_list_from_gs[0][5])
        self.assertEqual('link', ads_list_from_gs[0][6])
        self.assertEqual('kp', ads_list_from_gs[0][7])
        self.assertEqual('address', ads_list_from_gs[0][8])
        self.assertEqual('kadastr_list', ads_list_from_gs[0][9])
        self.assertEqual('ads_owner', ads_list_from_gs[0][10])
        self.assertEqual('ads_owner_id', ads_list_from_gs[0][11])
        self.assertEqual('first_parse_datetime', ads_list_from_gs[0][12])
        self.assertEqual('description', ads_list_from_gs[0][13])

    def test_saving_many_ads(self):
        new_ads_url = "https://docs.google.com/spreadsheets/d/1PMfgsa1wN1eWtwCCIWOCwTH1HQpz3Jb4o746Qc8UfLw"
        sheets_id = new_ads_url[39:]
        credentials_file = '../creds/google_creds.json'

        ads_list = []
        for i in range(0, 20):
            ads_uuid = str(uuid.uuid4())
            ads = self.create_test_ads1(ads_uuid)
            ads_list.append(ads)

        gs_ads_worker = GoogleSheetsWorker()
        gs_ads_worker.save_ads(ads_list, sheets_id, credentials_file, "ManyAds")
        ads_list_from_gs = gs_ads_worker.load_ads(sheets_id, credentials_file, "ManyAds")
        self.assertEqual(20, len(ads_list_from_gs))

    def test_saving_price_sotka(self):
        ads_uuid = str(uuid.uuid4())
        ads = self.create_test_ads1(ads_uuid)
        ads_list = [ads]

        new_ads_url = "https://docs.google.com/spreadsheets/d/1PMfgsa1wN1eWtwCCIWOCwTH1HQpz3Jb4o746Qc8UfLw"
        sheets_id = new_ads_url[39:]
        credentials_file = '../creds/google_creds.json'

        gs_ads_worker = GoogleSheetsWorker()
        gs_ads_worker.save_ads(ads_list, sheets_id, credentials_file, "PriceSotka")
        ads_list_from_gs = gs_ads_worker.load_ads(sheets_id, credentials_file, "PriceSotka")
        self.assertEqual(ads_uuid, ads_list_from_gs[0][0])
        self.assertEqual(str(ads.sector_number), ads_list_from_gs[0][1])
        self.assertEqual(ads.title, ads_list_from_gs[0][2])
        self.assertEqual(str(ads.square), ads_list_from_gs[0][3])
        self.assertEqual(str(ads.price), ads_list_from_gs[0][4])
        self.assertEqual(str(round(ads.price/ads.square, 0)), ads_list_from_gs[0][5])

    def test_getting_ads_from_db_saving_to_sheet(self):
        pass

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
        ads.sector_number = 2
        return ads


if __name__ == '__main__':
    unittest.main()
