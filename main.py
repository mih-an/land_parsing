from pprint import pprint

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

spreadsheet_id = "10egVpV2wRPsEtVvWVmqncP0cSwFu2tvdickJkBdGbBI"

credentials_file = "tests/test_data/google_creds.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    credentials_file, {'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'}
)
http_auth = credentials.authorize(httplib2.Http())
service = build('sheets', 'v4', http=http_auth)

res = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))'
).execute()

sheet_index = 0
last_row = len(res['sheets'][0]['data'][0]['rowData'])
google_sheet_range = f"A1:B{last_row}"

values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range=google_sheet_range,
    majorDimension='ROWS'
).execute()

pprint(values)

print(values.get("values")[0][0])
print(values.get("values")[0][1])
print(values.get("values")[1][0])
print(values.get("values")[1][1])

