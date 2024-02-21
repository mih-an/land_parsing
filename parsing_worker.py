import random
import time
import creds
from datetime import datetime

from db.ads_database import AdsDataBase
from html_readers.cian_parser import CianParser
from loaders.html_loader import HtmlLoader
from loaders.link_helper import LinkHelper
from loaders.sector_list_loader import SectorListLoader


class ParsingWorker:
    def __init__(self):
        self.max_attempt = 3
        self.google_credentials_file = 'tests/test_data/google_creds.json'
        self.sector_list_url = "https://docs.google.com/spreadsheets/d/1ph9a4sfNmwIEZKbWGwLX5iDYnOx6B5qdHYtuyIFR7H4"
        self.google_sheets_id = self.sector_list_url[39:]
        self.proxies = {'http': f'{creds.login}:{creds.password}@{creds.ip}'}
        # remove sectors list to our own database
        self.sector_loader = SectorListLoader()
        self.cian_parser = CianParser()
        self.html_loader = HtmlLoader()
        self.html_loader.set_proxies(self.proxies)
        self.link_helper = LinkHelper()
        self.ads_db = AdsDataBase()

    def run(self):
        sectors = self.sector_loader.load_sectors(self.google_sheets_id, self.google_credentials_file)
        sector_list_copy = sectors.copy()

        while len(sector_list_copy) > 0:
            sector_link, sector_number = self.choose_sector_randomly(sector_list_copy)
            sector_link = self.link_helper.gen_new_unique_url(sector_link)
            sector_html = self.try_few_attempts_downloading_sector_page(sector_link, sector_number, 1)
            ads_list = self.parse_sector(sector_html, sector_number, 1)
            self.save_to_database(ads_list, sector_number, 1)

            pages_count = self.get_sector_pages_count(sector_html, sector_number)
            for page_number in range(2, pages_count + 1):
                page_link = self.get_page_link(page_number, sector_link)
                sector_html = self.try_few_attempts_downloading_sector_page(page_link, sector_number, page_number)
                ads_list = self.parse_sector(sector_html, sector_number, page_number)
                self.save_to_database(ads_list, sector_number, page_number)

            del sector_list_copy[sector_number]

    def get_page_link(self, page_number, sector_link):
        print("-" * 30)
        print(f"Loading page number: {page_number}...")
        page_link = self.cian_parser.get_page_link(sector_link, page_number)
        return page_link

    def get_sector_pages_count(self, sector_html, sector_number):
        pages_count = self.cian_parser.get_pages_count(sector_html)
        print(f"Sector number {sector_number} has {pages_count} pages")
        return pages_count

    def try_few_attempts_downloading_sector_page(self, sector_link, sector_number, page):
        attempt_number = 0
        sector_html = ''

        while attempt_number < self.max_attempt:
            try:
                sector_html = self.download_sector_page(sector_link, sector_number, page)
                attempt_number = self.max_attempt
            except Exception as exc:
                attempt_number += 1
                print(f"Failed loading sector number: {sector_number}, page_number: {page}. "
                      f"Trying again... Attempt № {attempt_number}")
                print(f'Error: {exc}')
                sleep_seconds = 10
                print(f'Sleeping for {sleep_seconds} seconds...')
                time.sleep(sleep_seconds)

        return sector_html

    def download_sector_page(self, sector_link, sector_number, page):
        print(f'Loading generated unique sector link... {sector_link}')
        response = self.html_loader.load_page(sector_link)
        html = response.text
        print(f"Sector {sector_number} page {page} loaded successfully!")

        sleep_seconds = random.randint(5, 7)
        print(f'Sleeping for {sleep_seconds} seconds...')
        time.sleep(sleep_seconds)

        return html

    @staticmethod
    def choose_sector_randomly(sectors_copy):
        print('=' * 100)
        print(f'Sectors left to download: {len(sectors_copy)}')
        sector_number = random.choice(list(sectors_copy.keys()))
        sector_link = sectors_copy[sector_number]
        print(f'Sector number: {sector_number}, sector link: {sector_link}')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        return sector_link, sector_number

    def save_to_database(self, ads_list, sector_number, page_number):
        try:
            self.ads_db.save(ads_list)
            print(f"Data from sector {sector_number} page {page_number} successfully saved to database")
        except Exception as exc:
            print(f"Error saving sector {sector_number} page {page_number} to database")
            print(f'Exception: {exc}')

    def parse_sector(self, sector_html, sector_number, page_number):
        try:
            ads_list, is_error_occurred = self.cian_parser.get_ads(sector_html)
            if is_error_occurred:
                self.save_sector_html_to_file(page_number, sector_html, sector_number)
            self.set_sector_number_and_parsing_time(ads_list, sector_number)
            return ads_list
        except Exception as exc:
            self.save_sector_html_to_file(page_number, sector_html, sector_number)
            print(f'Exception: {exc}')

    @staticmethod
    def save_sector_html_to_file(page_number, sector_html, sector_number):
        file_name = f'sector_{sector_number}_p{page_number}.html'
        with open(file_name, 'a') as html_file:
            html_file.write(sector_html)
        print(f"Error parsing sector {sector_number} page {page_number}. Html saved to the file: {file_name}")

    @staticmethod
    def set_sector_number_and_parsing_time(ads_list, sector_number):
        for ads in ads_list:
            ads.sector_number = sector_number
            ads.first_parse_datetime = datetime.now().replace(microsecond=0)
            ads.last_parse_datetime = ads.first_parse_datetime

