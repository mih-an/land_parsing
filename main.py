from loaders.sector_list_loader import SectorListLoader

test_sectors_url = "https://docs.google.com/spreadsheets/d/1ph9a4sfNmwIEZKbWGwLX5iDYnOx6B5qdHYtuyIFR7H4"
sheets_id = test_sectors_url[39:]
credentials_file = 'tests/test_data/google_creds.json'

sl = SectorListLoader()
sectors = sl.load_sectors(sheets_id, credentials_file)

for item in sectors.items():
    sector_number = item[0]
    sector_link = item[1]

    print(f'Sector number: {sector_number}, sector link: {sector_link}')

