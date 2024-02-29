import random
import time
import logging
from logging.handlers import RotatingFileHandler

import sentry_sdk

import creds
from datetime import datetime

from db.ads_database import AdsDataBase
from html_readers.captcha_solver import CaptchaSolver
from html_readers.cian_parser import CianParser
from loaders.html_loader import HtmlLoader
from loaders.link_helper import LinkHelper
from loaders.sector_list_loader import SectorListLoader

sentry_sdk.init(
    dsn="https://28d3bac9cbf32d0e556609bb5695fcff@o4506671233957888.ingest.sentry.io/4506671237365760",
    # Enable performance monitoring
    enable_tracing=True,
)


class ParsingWorker:
    def __init__(self):
        self.max_attempt = 3
        self.google_credentials_file = 'creds/google_creds.json'
        self.sector_list_url = "https://docs.google.com/spreadsheets/d/1ph9a4sfNmwIEZKbWGwLX5iDYnOx6B5qdHYtuyIFR7H4"
        self.google_sheets_id = self.sector_list_url[39:]
        self.proxies = {'http': f'{creds.proxy_login}:{creds.proxy_password}@{creds.proxy_ip}'}
        # todo remove sectors list to local file
        self.sector_loader = SectorListLoader()
        self.html_loader = HtmlLoader()
        self.html_loader.set_proxies(self.proxies)
        self.link_helper = LinkHelper()
        self.cian_parser = CianParser()
        self.ads_db = AdsDataBase()
        logger_name = "parsing_log"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        file_name = f'{logger_name}.log'
        handler = RotatingFileHandler(file_name, maxBytes=104857600, backupCount=5)
        formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s", datefmt='%d-%b-%y %H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.cian_parser.set_logger(self.logger)

    def run(self):
        self.logger.info("\n\nNew parsing job begins: " + ">" * 150)
        sectors = self.sector_loader.load_sectors(self.google_sheets_id, self.google_credentials_file)
        sector_list_copy = sectors.copy()

        while len(sector_list_copy) > 0:
            sector_link, sector_number = self.choose_sector_randomly(sector_list_copy)
            sector_link = self.link_helper.gen_new_unique_url(sector_link)
            sector_html = self.download_parse_save(sector_link, sector_number, 1)

            pages_count = self.get_sector_pages_count(sector_html, sector_number)
            for page_number in range(2, pages_count + 1):
                page_link = self.get_page_link(page_number, sector_link)
                self.download_parse_save(page_link, sector_number, page_number)

            del sector_list_copy[sector_number]

    def download_parse_save(self, link, sector_number, page_number):
        html = self.try_few_attempts_downloading_sector_page(link, sector_number, page_number)
        ads_list = self.parse_sector(html, sector_number, page_number)
        self.save_to_database(ads_list, sector_number, page_number)
        return html

    def get_page_link(self, page_number, sector_link):
        self.logger.info("-" * 30)
        self.logger.info(f"Loading page number: {page_number}...")
        page_link = self.cian_parser.get_page_link(sector_link, page_number)
        return page_link

    def get_sector_pages_count(self, sector_html, sector_number):
        pages_count = self.cian_parser.get_pages_count(sector_html)
        self.logger.info(f"Sector number {sector_number} has {pages_count} pages")
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
                self.logger.error(f"Failed loading sector number: {sector_number}, page_number: {page}. "
                                  f"Trying again... Attempt № {attempt_number}")
                self.logger.exception(exc)
                sleep_seconds = 10
                self.logger.info(f'Sleeping for {sleep_seconds} seconds...')
                time.sleep(sleep_seconds)

        return sector_html

    def download_sector_page(self, sector_link, sector_number, page):
        self.logger.info(f'Loading generated unique sector link... {sector_link}')
        response = self.html_loader.load_page(sector_link)
        html = response.text

        if self.cian_parser.has_captcha(html):
            self.logger.info(f"Captcha detected! Trying to solve it...")
            cs = CaptchaSolver()
            session = self.html_loader.get_session()
            response = cs.solve(sector_link, session)
            html = response.text

        self.logger.info(f"Sector {sector_number} page {page} loaded successfully!")

        sleep_seconds = random.randint(5, 10)
        self.logger.info(f'Sleeping for {sleep_seconds} seconds...')
        time.sleep(sleep_seconds)

        return html

    def choose_sector_randomly(self, sectors_copy):
        self.logger.info('=' * 100)
        self.logger.info(f'Sectors left to download: {len(sectors_copy)}')
        sector_number = random.choice(list(sectors_copy.keys()))
        sector_link = sectors_copy[sector_number]
        self.logger.info(f'Sector number: {sector_number}, sector link: {sector_link}')

        return sector_link, sector_number

    def save_to_database(self, ads_list, sector_number, page_number):
        try:
            self.ads_db.save(ads_list)
            self.logger.info(f"Data from sector {sector_number} page {page_number} successfully saved to database")
        except Exception as exc:
            self.logger.error(f"Error saving sector {sector_number} page {page_number} to database")
            self.logger.exception(exc)

    def parse_sector(self, sector_html, sector_number, page_number):
        try:
            ads_list, is_error_occurred = self.cian_parser.get_ads(sector_html)
            self.set_sector_number_and_parsing_time(ads_list, sector_number)
            if not is_error_occurred:
                self.logger.info(f"Data from sector {sector_number} page {page_number} successfully parsed")
            else:
                self.save_sector_html_to_file(page_number, sector_html, sector_number)
            return ads_list
        except Exception as exc:
            self.save_sector_html_to_file(page_number, sector_html, sector_number)
            self.logger.exception(exc)

    def save_sector_html_to_file(self, page_number, sector_html, sector_number):
        file_name = f'sector_{sector_number}_p{page_number}.html'
        with open(file_name, 'a') as html_file:
            html_file.write(sector_html)
        self.logger.info(
            f"Error parsing sector {sector_number} page {page_number}. Html saved to the file: {file_name}")

    @staticmethod
    def set_sector_number_and_parsing_time(ads_list, sector_number):
        for ads in ads_list:
            ads.sector_number = sector_number
            ads.first_parse_datetime = datetime.now().replace(microsecond=0)
            ads.last_parse_datetime = ads.first_parse_datetime
