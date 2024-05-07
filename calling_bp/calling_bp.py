from db.ads_database import AdsDataBase
from loaders.ads_checker import AdsChecker


class CallBusinessProcess:
    def __init__(self):
        self.ads_db = AdsDataBase()

    def save_to_call(self, ads_list):
        self.ads_db.save_to_call(ads_list)

    def load_ads_list_to_call(self):
        return self.ads_db.select_ads_to_call()

    def insert_portion_to_call(self):
        ads_list = self.ads_db.select_portion_to_call()
        ads_checker = AdsChecker()
        for ads in ads_list:
            ads_checker.check_ads(ads)

        self.ads_db.insert_portion_to_call()

    def check_ads_to_call(self, ads_id):
        return self.ads_db.select_one_ads_to_call(ads_id)
