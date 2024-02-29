import os
from twocaptcha.solver import TwoCaptcha
import creds


class CaptchaSolver:
    def __init__(self):
        self.api_key = os.getenv('APIKEY_2CAPTCHA', creds.rucaptcha_key)
        self.solver = TwoCaptcha(self.api_key)
        self.cian_site_key = '6LdpqSQUAAAAAJXo9mQJY2QYw2rSi2D0-ZXctcw_'
        self.redirect_str = '?redirect_url='
        self.cian_captcha_post_url = "https://www.cian.ru/captcha/"
        self.captcha_url = self.cian_captcha_post_url + self.redirect_str

    def solve(self, redirect_url, session):
        solving_result = self.solver.recaptcha(sitekey=self.cian_site_key, url=self.captcha_url + redirect_url)
        data = {'g-recaptcha-response': solving_result['code'], 'redirect_url': '/'}
        session.post(self.cian_captcha_post_url, data)

        return solving_result
