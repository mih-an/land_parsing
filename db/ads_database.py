from mysql.connector import connect, Error
import creds
from html_readers.ads import Ads, AdsPriceHistoryItem


class AdsDataBase:
    def __init__(self):
        self.select_new_ads_last_2_days_query = """
            SELECT ads_id, ads_title, square, price, vri, link, kp, address, description, kadastr, 
                electronic_trading, ads_owner, ads_owner_id, first_parse_datetime, sector_number, last_parse_datetime 
            FROM ads
            WHERE DATE(first_parse_datetime) > DATE(NOW()) - INTERVAL 2 DAY 
                AND ads_owner <> 'Застройщик' AND square >= 12
            ORDER BY DATE(first_parse_datetime) DESC, sector_number"""
        self.select_new_ads_last_ten_days_query = """
            SELECT ads_id, ads_title, square, price, vri, link, kp, address, description, kadastr, 
                electronic_trading, ads_owner, ads_owner_id, first_parse_datetime, sector_number, last_parse_datetime 
            FROM ads
            WHERE DATE(first_parse_datetime) > DATE(NOW()) - INTERVAL 10 DAY 
                AND ads_owner <> 'Застройщик' AND square >= 12
            ORDER BY DATE(first_parse_datetime) DESC, sector_number"""
        self.delete_test_ads_query = """DELETE FROM ads WHERE LENGTH(ads_id) = 36"""
        self.select_ads_price_history_query = """
            SELECT ads_id, price, price_datetime 
            FROM ads_price_history
            WHERE ads_id = %s
        """
        self.insert_old_ads_new_prices_to_history_query = """
            INSERT INTO ads_price_history (ads_id, price, price_datetime)
            SELECT tmp_ads.ads_id, tmp_ads.price,tmp_ads.first_parse_datetime
            FROM tmp_ads INNER JOIN ads ON tmp_ads.ads_id = ads.ads_id
            WHERE tmp_ads.price <> ads.price;
        """
        self.insert_ads_prices_to_history_query = """
            INSERT INTO ads_price_history (ads_id, price, price_datetime)
            SELECT ads_id, price, first_parse_datetime
            FROM tmp_ads 
            WHERE ads_id not in (SELECT ads_id FROM ads)
        """
        self.select_one_ads_by_id_query = """
            SELECT ads_id, ads_title, square, price, vri, link, kp, address, description, kadastr, 
                electronic_trading, ads_owner, ads_owner_id, first_parse_datetime, sector_number, 
                last_parse_datetime 
            FROM ads WHERE ads_id = %s 
        """
        self.insert_tmp_ads_query = """
            INSERT INTO tmp_ads (ads_id, ads_title, square, price, vri, link, kp, address, description, 
                kadastr, electronic_trading, ads_owner, ads_owner_id, first_parse_datetime, sector_number,
                last_parse_datetime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.insert_new_ads_to_main_table_query = """
            INSERT INTO ads(ads_id, ads_title, square, price, vri, link, kp, address, description, kadastr,
                electronic_trading, ads_owner, ads_owner_id, first_parse_datetime, sector_number, last_parse_datetime)
            SELECT ads_id, ads_title, square, price, vri, link, kp, address, description, kadastr, 
                electronic_trading, ads_owner, ads_owner_id, first_parse_datetime, sector_number, 
                last_parse_datetime
            FROM tmp_ads
            WHERE ads_id not in (SELECT ads_id FROM ads)
        """
        self.delete_from_tmp_ads_query = """
            DELETE FROM tmp_ads
        """
        self.update_ads_prices_and_parsing_time_query = """
            UPDATE ads, tmp_ads
            SET ads.price = tmp_ads.price, ads.last_parse_datetime = tmp_ads.last_parse_datetime
            WHERE ads.ads_id = tmp_ads.ads_id;
        """
        self.kadastr_separator = ','

    def save(self, ads_list):
        if ads_list is None or len(ads_list) == 0:
            return

        # We need to separate ads for 2 groups:
        # 1. New ones
        # 2. Already existed
        # We do it with temporary table. Otherwise, it will be too slow in the future
        try:
            self.insert_ads_to_tmp_table(ads_list)
        except Error as e:
            print(f'Error saving ads list to tmp table: {e}')
            raise e

        # Save new ads prices to price history table
        # This code should be executed before saving new ads to main table - self.insert_new_ads_to_main_table()
        # Otherwise, ads won't be "new" from the database perspective
        try:
            self.insert_new_ads_prices_to_history()
        except Error as e:
            print(f'Error inserting ads prices to history: {e}')
            raise e

        # Save new ads to main table
        try:
            self.insert_new_ads_from_tmp_to_main_table()
        except Error as e:
            print(f'Error saving ads list to main table: {e}')
            raise e

        # Save old ads new prices to price history table
        try:
            self.insert_old_ads_new_prices_to_history()
        except Error as e:
            print(f'Error inserting old ads new prices to history: {e}')
            raise e

        # Update prices for old ads in the main table and also update parsing time
        try:
            self.update_old_ads_prices_and_parsing_time()
        except Error as e:
            print(f'Error updating ads prices: {e}')
            raise e

        # Clear tmp table
        try:
            self.delete_from_tmp_ads()
        except Error as e:
            print(f'Error deleting from tmp ads table: {e}')
            raise e

    def execute_insert_query(self, ads_list, insert_query):
        with connect(
                host=creds.db_host,
                user=creds.db_user,
                password=creds.db_password,
                database=creds.db_name,
        ) as connection:
            ads_records = self.get_records_from_ads(ads_list)
            with connection.cursor() as cursor:
                cursor.executemany(insert_query, ads_records)
                connection.commit()

    def insert_new_ads_from_tmp_to_main_table(self):
        self.execute_query(self.insert_new_ads_to_main_table_query)

    def insert_ads_to_tmp_table(self, ads_list):
        self.execute_insert_query(ads_list, self.insert_tmp_ads_query)

    def get_records_from_ads(self, ads_list):
        ads_records = []
        for ads in ads_list:
            ads_records.append([ads.id, ads.title, ads.square, ads.price, ads.vri, ads.link, ads.kp, ads.address,
                                ads.description, self.kadastr_separator.join(ads.kadastr_list),
                                ads.electronic_trading, ads.ads_owner, ads.ads_owner_id, ads.first_parse_datetime,
                                ads.sector_number, ads.last_parse_datetime])
        return ads_records

    def select_ads_by_id(self, ads_id):
        try:
            with connect(
                    host=creds.db_host,
                    user=creds.db_user,
                    password=creds.db_password,
                    database=creds.db_name,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self.select_one_ads_by_id_query, [ads_id])
                    for ads_from_db in cursor.fetchall():
                        return self.get_ads_from_db_record(ads_from_db)
        except Error as e:
            print(f'Error getting ads from database: {e}')

    def get_ads_from_db_record(self, ads_record_from_db):
        ads = Ads()
        ads.id = ads_record_from_db[0]
        ads.title = ads_record_from_db[1]
        ads.square = ads_record_from_db[2]
        ads.price = ads_record_from_db[3]
        ads.vri = ads_record_from_db[4]
        ads.link = ads_record_from_db[5]
        ads.kp = ads_record_from_db[6]
        ads.address = ads_record_from_db[7]
        ads.description = ads_record_from_db[8]
        if ads_record_from_db[9] == '':
            ads.kadastr_list = []
        else:
            ads.kadastr_list = ads_record_from_db[9].split(self.kadastr_separator)
        ads.electronic_trading = ads_record_from_db[10]
        ads.is_electronic_trading = not ads.electronic_trading == ''
        ads.ads_owner = ads_record_from_db[11]
        ads.ads_owner_id = ads_record_from_db[12]
        ads.first_parse_datetime = ads_record_from_db[13]
        ads.sector_number = ads_record_from_db[14]
        ads.last_parse_datetime = ads_record_from_db[15]
        return ads

    def select_price_history(self, ads_uuid):
        price_items_list = []
        with connect(
                host=creds.db_host,
                user=creds.db_user,
                password=creds.db_password,
                database=creds.db_name,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.select_ads_price_history_query, [ads_uuid])
                for price_item_from_db in cursor.fetchall():
                    price_item = AdsPriceHistoryItem()
                    price_item.ads_id = price_item_from_db[0]
                    price_item.price = price_item_from_db[1]
                    price_item.price_datetime = price_item_from_db[2]
                    price_items_list.append(price_item)
        return price_items_list

    @staticmethod
    def execute_query(query):
        with connect(
                host=creds.db_host,
                user=creds.db_user,
                password=creds.db_password,
                database=creds.db_name,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()

    def update_old_ads_prices_and_parsing_time(self):
        self.execute_query(self.update_ads_prices_and_parsing_time_query)

    def insert_new_ads_prices_to_history(self):
        self.execute_query(self.insert_ads_prices_to_history_query)

    def insert_old_ads_new_prices_to_history(self):
        self.execute_query(self.insert_old_ads_new_prices_to_history_query)

    def delete_from_tmp_ads(self):
        self.execute_query(self.delete_from_tmp_ads_query)

    def delete_test_ads(self):
        self.execute_query(self.delete_test_ads_query)

    def select_new_ads_last_ten_days(self):
        try:
            with connect(
                    host=creds.db_host,
                    user=creds.db_user,
                    password=creds.db_password,
                    database=creds.db_name,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self.select_new_ads_last_ten_days_query)
                    ads_list = []
                    for ads_from_db in cursor.fetchall():
                        ads = self.get_ads_from_db_record(ads_from_db)
                        ads_list.append(ads)
                    return ads_list
        except Error as e:
            print(f'Error getting new ads for last ten days from database: {e}')

    def select_new_ads_last_2_days(self):
        try:
            with connect(
                    host=creds.db_host,
                    user=creds.db_user,
                    password=creds.db_password,
                    database=creds.db_name,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self.select_new_ads_last_2_days_query)
                    ads_list = []
                    for ads_from_db in cursor.fetchall():
                        ads = self.get_ads_from_db_record(ads_from_db)
                        ads_list.append(ads)
                    return ads_list
        except Error as e:
            print(f'Error getting new ads for last ten days from database: {e}')
