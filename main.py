import time
import random

from html_readers.cian_parcer import CianParser
from loaders.land_parser import LandParser
from loaders.sector_list_loader import SectorListLoader

test_sectors_url = "https://docs.google.com/spreadsheets/d/1ph9a4sfNmwIEZKbWGwLX5iDYnOx6B5qdHYtuyIFR7H4"
sheets_id = test_sectors_url[39:]
credentials_file = 'tests/test_data/google_creds.json'

sector_loader = SectorListLoader()
sectors = sector_loader.load_sectors(sheets_id, credentials_file)

ip = '31.28.11.181:41552'
login = 'Megafon1527_2'
password = 'AzsILk'
max_attempt = 3

proxies = {
    'https': f'{login}:{password}@{ip}'
}

land_parser = LandParser()
land_parser.set_proxies(proxies)
cian_parser = CianParser()

for item in sectors.items():
    sector_number = item[0]
    sector_link = item[1]

    print(f'Sector number: {sector_number}, sector link: {sector_link}')

    attempt_number = 0
    while attempt_number < max_attempt:
        try:
            response = land_parser.load_page(sector_link)
            html = response.text
            file_name = f'sector_{sector_number}_p1.html'
            with open(file_name, 'a') as html_file:
                html_file.write(html)
            print(f"Successfully loaded sector page number {sector_number} and saved to file {file_name}")

            pages_count = cian_parser.get_pages_count(html)

            print('Sleeping for 4-6 seconds randomly')
            time.sleep(random.randint(4, 6))
            attempt_number = max_attempt
        except Exception as exc:
            print(f'Error: {exc}')
            print(f"Failed loading sector page number: {sector_number}. Trying again...")
            attempt_number += 1
