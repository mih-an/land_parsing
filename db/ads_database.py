from mysql.connector import connect, Error
from datetime import datetime
import creds
from html_readers.cian_parcer import Ads


class AdsDataBase:
    def __init__(self):
        self.select_ads_query = """
            SELECT ads_id, ads_title, square, price, vri, link, locality, kp, address, description, kadastr, 
                electronic_trading, ads_owner, ads_owner_id, ads_first_parce_datetime 
            FROM ads WHERE ads_id = %s 
        """
        self.insert_ads_query = """
            INSERT INTO ads (ads_id, ads_title, square, price, vri, link, locality, kp, address, description, kadastr, 
                electronic_trading, ads_owner, ads_owner_id, ads_first_parce_datetime)
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.kadastr_separator = ','

    def save(self, ads_list):
        try:
            with connect(
                    host=creds.db_host,
                    user=creds.db_user,
                    password=creds.db_password,
                    database=creds.db_name,
            ) as connection:
                ads_records = self.get_ads_records(ads_list)
                with connection.cursor() as cursor:
                    cursor.executemany(self.insert_ads_query, ads_records)
                    connection.commit()
        except Error as e:
            print(f'Error saving ads list to database: {e}')

    def get_ads_records(self, ads_list):
        ads_records = []
        for ads in ads_list:
            ads_records.append([ads.id, ads.title, ads.square, ads.price, ads.vri, ads.link, ads.locality,
                                ads.kp, ads.address, ads.description,
                                self.kadastr_separator.join(ads.kadastr_list),
                                ads.electronic_trading, ads.ads_owner, ads.ads_owner_id,
                                datetime.now()])
        return ads_records

    def get_ads_by_id(self, ads_id):
        try:
            with connect(
                    host=creds.db_host,
                    user=creds.db_user,
                    password=creds.db_password,
                    database=creds.db_name,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self.select_ads_query, [ads_id])
                    for ads_from_db in cursor.fetchall():
                        return self.get_ads_from_db_record(ads_from_db)
        except Error as e:
            print(f'Error saving ads list to database: {e}')

    def get_ads_from_db_record(self, ads_from_db):
        ads = Ads()
        ads.id = ads_from_db[0]
        ads.title = ads_from_db[1]
        ads.square = ads_from_db[2]
        ads.price = ads_from_db[3]
        ads.vri = ads_from_db[4]
        ads.link = ads_from_db[5]
        ads.locality = ads_from_db[6]
        ads.kp = ads_from_db[7]
        ads.address = ads_from_db[8]
        ads.description = ads_from_db[9]
        if ads_from_db[10] == '':
            ads.kadastr_list = []
        else:
            ads.kadastr_list = ads_from_db[10].split(self.kadastr_separator)
        ads.electronic_trading = ads_from_db[11]
        ads.is_electronic_trading = not ads.electronic_trading == ''
        ads.ads_owner = ads_from_db[12]
        ads.ads_owner_id = ads_from_db[13]
        return ads


