import time
from datetime import datetime

from db.ads_database import AdsDataBase
from html_readers.captcha_solver import CaptchaSolver
from html_readers.cian_parser import CianParser
from loaders.html_loader import HtmlLoader


class AdsChecker:
    def __init__(self):
        self.html_loader = HtmlLoader()
        self.cian_parser = CianParser()
        self.ads_db = AdsDataBase()

    def check_ads(self, ads):
        # for testing purposes
        if ads.link == 'dont_check':
            return ads.is_unpublished

        # don't check new ads
        now = datetime.now().replace(microsecond=0)
        delta = now - ads.last_parse_datetime
        if delta.days <= 1:
            return ads.is_unpublished

        response = self.html_loader.load_page(ads.link)
        html = response.text

        if self.cian_parser.has_captcha(html):
            session = self.html_loader.get_session()
            cs = CaptchaSolver()
            cs.solve(ads.link, session)
            response = self.html_loader.load_page(ads.link)
            html = response.text

        sleep_seconds = 10
        time.sleep(sleep_seconds)

        ads.is_unpublished = self.cian_parser.is_unpublished(html)
        self.ads_db.save_published_status(ads)

        return ads.is_unpublished


