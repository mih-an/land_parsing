import random
import time
from datetime import datetime

from db.ads_database import AdsDataBase
from html_readers.captcha_solver import CaptchaSolver
from html_readers.cian_parser import CianParser
from loaders.html_loader import HtmlLoader


class AdsChecker:
    def __init__(self):
        self.logger = None
        self.max_attempt = 3
        self.html_loader = HtmlLoader()
        self.cian_parser = CianParser()
        self.ads_db = AdsDataBase()

    def set_logger(self, logger):
        self.logger = logger

    def check_ads(self, ads):
        # for testing purposes
        if ads.link == 'dont_check':
            return ads.is_unpublished

        # don't check new ads
        now = datetime.now().replace(microsecond=0)
        delta = now - ads.last_parse_datetime
        if delta.days <= 1:
            if self.logger is not None:
                self.logger.info(f"Ads with id {ads.id} is fresh. No need to check for unpublished status ")
            return ads.is_unpublished

        html = self.try_few_attempts_downloading_page(ads.link)
        ads.is_unpublished = self.cian_parser.is_unpublished(html)
        self.ads_db.save_published_status(ads)

        return ads.is_unpublished

    def try_few_attempts_downloading_page(self, link):
        attempt_number = 0
        html = ''

        while attempt_number < self.max_attempt:
            try:
                if self.logger is not None:
                    self.logger.info(f"Trying to load ads link {link}")
                response = self.html_loader.load_page(link)
                html = response.text
                if self.cian_parser.has_captcha(html):
                    if self.logger is not None:
                        self.logger.info(f"Response has a captcha! Trying to solve it...")
                    session = self.html_loader.get_session()
                    cs = CaptchaSolver()
                    cs.solve(link, session)
                    if self.logger is not None:
                        self.logger.info(f"Captcha successfully solved!")
                    response = self.html_loader.load_page(link)
                    html = response.text
                attempt_number = self.max_attempt

                if self.logger is not None:
                    self.logger.info(f"Ads link {link} loaded successfully!")
                sleep_seconds = random.randint(5, 10)
                if self.logger is not None:
                    self.logger.info(f'Sleeping for {sleep_seconds} seconds...')
                time.sleep(sleep_seconds)

            except Exception as exc:
                attempt_number += 1
                if self.logger is not None:
                    self.logger.error(f"Failed loading ads link: {link}. Trying again... Attempt № {attempt_number}")
                if self.logger is not None:
                    self.logger.exception(exc)
                sleep_seconds = 10
                if self.logger is not None:
                    self.logger.info(f'Sleeping for {sleep_seconds} seconds...')
                time.sleep(sleep_seconds)

        return html


