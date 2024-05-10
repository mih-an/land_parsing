import datetime
import decimal


class AdsPriceHistoryItem:
    ads_id: int = None
    price: int = None
    price_datetime: datetime = None


class Ads:
    square = 0
    title = ''
    price = 0
    vri = ''
    link = ''
    id = ''
    kp = ''
    address1 = ''
    address2 = ''
    address3 = ''
    address = ''
    description = ''
    ads_owner = ''
    ads_owner_id = ''
    electronic_trading = ''
    is_electronic_trading = False
    kadastr_list: list[str] = []
    first_parse_datetime: datetime = None
    last_parse_datetime: datetime = None
    sector_number: int = None
    is_unpublished = False
    to_call_datetime: datetime = None

    def get_price_sotka(self):
        if self.square == 0:
            return 0
        else:
            return round(float(self.price / decimal.Decimal(self.square)))
