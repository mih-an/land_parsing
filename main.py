import mechanicalsoup
browser = mechanicalsoup.Browser()
# url = "http://olympus.realpython.org/login"
url = "https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=3&offer_type=suburban&p=2&region=4593"
page = browser.get(url)
print(page.soup)
