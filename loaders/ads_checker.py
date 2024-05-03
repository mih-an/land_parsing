from html_readers.cian_parser import CianParser
from loaders.html_loader import HtmlLoader


class AdsChecker:
    def __init__(self):
        self.html_loader = HtmlLoader()
        self.cian_parser = CianParser()

    def check_ads(self, ads):
        response = self.html_loader.load_page(ads.link)
        html = response.text
        # todo check captcha
        is_unpublished = self.cian_parser.is_unpublished(html)
        return is_unpublished

        # save status to database

