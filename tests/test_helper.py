from html_readers.ads import Ads


class TestHelper:
    @staticmethod
    def create_test_ads1(ads_uuid):
        ads = Ads()
        ads.title = 'Участок, 9.9 сот., Садоводство'
        ads.square = 9.9
        ads.price = 1800000
        ads.vri = 'Садоводство'
        ads.link = 'https://istra.cian.ru/sale/suburban/281048577/'
        ads.id = ads_uuid
        ads.kp = 'Майские дачи 2'
        ads.address = 'Московская область, Истра городской округ, Майские Дачи кп'
        ads.description = 'Самое крутое объявление'
        ads.kadastr_list = ['50:08:0040229:1139', '50:08:0040229:1165']
        ads.electronic_trading = 'Электронные торги'
        ads.is_electronic_trading = True
        ads.ads_owner = 'Собственник'
        ads.ads_owner_id = 'ID 70642111'
        ads.first_parse_datetime = datetime.now().replace(microsecond=0)
        ads.last_parse_datetime = ads.first_parse_datetime
        ads.sector_number = 1
        return ads

    @staticmethod
    def create_test_ads2(ads_uuid):
        ads = Ads()
        ads.title = 'Участок, 6 сот.'
        ads.square = 6
        ads.price = 425000
        ads.vri = ''
        ads.link = 'https://istra.cian.ru/sale/suburban/287210218/'
        ads.id = ads_uuid
        ads.kp = 'КП «‎Прилесные дачи »'
        ads.address = 'Московская область, Истра городской округ, д. Малое Ушаково'
        ads.description = 'Самое крутое объявление 2'
        ads.kadastr_list = ['50:08:0040229:85']
        ads.ads_owner = 'Риелтор'
        ads.ads_owner_id = 'ID 23674176'
        ads.first_parse_datetime = datetime.now().replace(microsecond=0)
        ads.last_parse_datetime = ads.first_parse_datetime
        ads.sector_number = 2
        return ads
