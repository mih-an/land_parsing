from pprint import pprint

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class SectorListLoader:

    def __init__(self):
        self.spreadsheet_id = None

    def load_sectors(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        credentials_file = '../tests/test_data/google_creds.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file, {'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'}
        )
        http_auth = credentials.authorize(httplib2.Http())
        service = build('sheets', 'v4', http=http_auth)

        res = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields='sheets(data/rowData/values/userEnteredValue,properties(index))'
        ).execute()
        last_row = len(res['sheets'][0]['data'][0]['rowData'])
        google_sheet_range = f"A1:B{last_row}"

        values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=google_sheet_range).execute()

        sector_list = {}
        for i in range(last_row):
            sector_number = values.get("values")[i][0]
            sector_link = values.get("values")[i][1]
            sector_list[sector_number] = sector_link

        return sector_list
