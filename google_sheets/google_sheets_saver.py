import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetsWorker:
    def __init__(self):
        self.kadastr_separator = ','
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        self.credentials_file = 'creds/google_creds.json'

    def save_ads(self, ads_list, sheet_id, credentials_file, sheet_name):
        creds = Credentials.from_service_account_file(credentials_file, scopes=self.scopes)
        client = gspread.authorize(creds)
        workbook = client.open_by_key(sheet_id)

        worksheet_list = map(lambda x: x.title, workbook.worksheets())
        if sheet_name in worksheet_list:
            sheet = workbook.worksheet(sheet_name)
        else:
            sheet = workbook.add_worksheet(sheet_name, rows=10, cols=15)

        sheet.clear()
        ads_records = []
        self.add_headers(ads_records)
        self.get_records_from_ads_to_gs(ads_list, ads_records)
        sheet.update(range_name=f"A1:O{len(ads_records)}", values=ads_records)

    def get_records_from_ads_to_gs(self, ads_list, ads_records):
        for ads in ads_list:
            ads_records.append([ads.id, ads.sector_number, ads.title, ads.square, ads.price,
                                str(ads.get_price_sotka()), ads.vri, ads.link, ads.kp,
                                ads.address, self.kadastr_separator.join(ads.kadastr_list), ads.ads_owner,
                                ads.ads_owner_id, str(ads.first_parse_datetime), ads.description])
        return ads_records

    def load_ads_with_title(self, sheet_id, credentials_file, sheet_name):
        creds = Credentials.from_service_account_file(credentials_file, scopes=self.scopes)
        client = gspread.authorize(creds)
        workbook = client.open_by_key(sheet_id)

        worksheet_list = map(lambda x: x.title, workbook.worksheets())
        if sheet_name in worksheet_list:
            sheet = workbook.worksheet(sheet_name)
        else:
            sheet = workbook.add_worksheet(sheet_name, rows=10, cols=10)

        list_of_lists = sheet.get_all_values()
        return list_of_lists

    def load_ads(self, sheets_id, credentials_file, sheet_name):
        ads_with_title = self.load_ads_with_title(sheets_id, credentials_file, sheet_name)
        return ads_with_title[1:]

    @staticmethod
    def add_headers(ads_records):
        ads_records.append(['id', 'sector_number', 'title', 'square', 'price', 'price_sotka', 'vri', 'link', 'kp',
                            'address', 'kadastr_list', 'ads_owner', 'ads_owner_id', 'first_parse_datetime',
                            'description'])

