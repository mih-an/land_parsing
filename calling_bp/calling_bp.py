from db.ads_database import AdsDataBase


class CallBusinessProcess:
    def __init__(self):
        self.ads_db = AdsDataBase()

    def save_to_call(self, ads_list):
        self.ads_db.save_to_call(ads_list)

    def load_ads_list_to_call(self):
        return self.ads_db.select_ads_to_call()
