from db.ads_database import AdsDataBase
from loaders.ads_checker import AdsChecker


class CallBusinessProcess:
    def __init__(self):
        self.ads_db = AdsDataBase()

    def save_to_call(self, ads_list):
        self.ads_db.save_to_call(ads_list)

    def load_ads_list_to_call(self):
        return self.ads_db.select_ads_to_call()

    def check_ads_to_call(self, ads_id):
        return self.ads_db.select_one_ads_to_call(ads_id)

    def load_ads_to_call_by_date(self, date):
        return self.ads_db.select_ads_to_call_by_date(date)

    # it should be only this one method to insert ads to call
    def insert_ads_to_call(self, ads_count_to_call, date_to_call):
        # Берем с запасом, так как часть окажется уже снятой с публикации
        count = ads_count_to_call * 2
        ads_list = self.ads_db.select_n_ads_to_call(count)

        ads_list_to_call = []
        if ads_count_to_call > len(ads_list):
            ads_count_to_call = len(ads_list)

        ads_checker = AdsChecker()
        i = 0
        while i < ads_count_to_call:
            ads_to_call = ads_list[i]
            is_unpublished = ads_checker.check_ads(ads_to_call)

            if is_unpublished:
                del ads_list[i]
                if ads_count_to_call > len(ads_list):
                    ads_count_to_call = len(ads_list)
                continue

            ads_list_to_call.append(ads_to_call)
            i += 1

        self.ads_db.save_to_call(ads_list_to_call)



