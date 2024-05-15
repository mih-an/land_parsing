import datetime
import logging

from logging.handlers import RotatingFileHandler
from db.ads_database import AdsDataBase
from google_sheets.google_sheets_saver import GoogleSheetsWorker
from loaders.ads_checker import AdsChecker


class CallBusinessProcess:
    def __init__(self):
        self.sheet_name = "ToCall"
        self.ads_db = AdsDataBase()
        self.new_ads_url = "https://docs.google.com/spreadsheets/d/1yGezEPbzYSGHnSJeLwuteI7zLUaM6g5CSWDiFNhstZQ"
        self.sheets_id = self.new_ads_url[39:]
        self.credentials_file = '../creds/google_creds.json'
        self.gs_ads_worker = GoogleSheetsWorker()

        logger_name = "parsing_log"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        file_name = f'{logger_name}.log'
        handler = RotatingFileHandler(file_name, maxBytes=104857600, backupCount=5)
        formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s", datefmt='%d-%b-%y %H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def save_to_call(self, ads_list):
        self.ads_db.save_to_call(ads_list)

    def check_ads_to_call(self, ads_id):
        return self.ads_db.select_one_ads_to_call(ads_id)

    # it should be only this one method to insert ads to call
    def insert_ads_to_call(self, ads_count_to_call, date_to_call, save_to_gs=False):
        # Берем с запасом, так как часть окажется уже снятой с публикации
        count = ads_count_to_call * 2
        ads_list = self.ads_db.select_n_ads_to_call(count)
        self.logger.info(f"Start inserting to call. Selected ads to check before calling  - {len(ads_list)}")

        ads_list_to_call = []
        if ads_count_to_call > len(ads_list):
            ads_count_to_call = len(ads_list)

        if date_to_call is None:
            date_to_call = datetime.datetime.now().date()

        if ads_count_to_call == 0:
            self.logger.info("Nothing add to call...")

        ads_checker = AdsChecker()
        ads_checker.set_logger(self.logger)
        i = 0
        while i < ads_count_to_call:
            ads_to_call = ads_list[i]
            self.logger.info(f"Ads {i} id {ads_to_call.id} - checking {ads_to_call.link}")
            is_unpublished = ads_checker.check_ads(ads_to_call)

            if is_unpublished:
                self.logger.info(f"{ads_to_call.link} is unpublished already")
                del ads_list[i]
                if ads_count_to_call > len(ads_list):
                    ads_count_to_call = len(ads_list)
                continue

            ads_to_call.to_call_datetime = date_to_call
            ads_list_to_call.append(ads_to_call)
            self.logger.info(f"{ads_to_call.link} checked and added to call")
            i += 1

        self.logger.info(f"Saving ads to call - {len(ads_list_to_call)}")
        self.ads_db.save_to_call(ads_list_to_call)
        if save_to_gs:
            self.logger.info(f"Saving ads to call to google sheets - {len(ads_list_to_call)}")
            self.gs_ads_worker.append_ads(ads_list_to_call, self.sheets_id, self.credentials_file, self.sheet_name)

    def load_ads_list_to_call(self):
        return self.ads_db.select_ads_to_call()

    # Method accepts only date without time!
    def load_ads_list_to_call_by_date(self, date):
        return self.ads_db.select_ads_to_call_by_date(date)



