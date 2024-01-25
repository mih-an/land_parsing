import time
import random

from html_readers.cian_parcer import CianParser
from loaders.land_parser import HtmlLoader
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

html_loader = HtmlLoader()
html_loader.set_proxies(proxies)
cian_parser = CianParser()

sectors_copy = sectors.copy()

# Looping all sectors randomly
while len(sectors_copy) > 0:
    print(f'length: {len(sectors_copy.items())}')
    sector_number = random.choice(list(sectors_copy.keys()))
    sector_link = sectors_copy[sector_number]
    print(f'sector number: {sector_number}, sector link: {sector_link}')

    attempt_number = 0
    while attempt_number < max_attempt:
        try:
            response = html_loader.load_page(sector_link)
            html = response.text
            file_name = f'sector_{sector_number}_p1.html'
            with open(file_name, 'a') as html_file:
                html_file.write(html)
            print(f"Successfully loaded sector page number {sector_number} and saved to file {file_name}")

            pages_count = cian_parser.get_pages_count(html)
            print(f"Sector number {sector_number} has {pages_count} pages")
            for i in range(2, pages_count+1):
                page_link = cian_parser.get_page_link(sector_link, i)
                print("-"*30)
                print(f"Loading page number: {i}")

            sleep_seconds = random.randint(4, 6)
            print(f'Sleeping for {sleep_seconds} seconds randomly')
            time.sleep(sleep_seconds)

            attempt_number = max_attempt
            del sectors_copy[sector_number]

        except Exception as exc:
            print(f'Error: {exc}')
            print(f"Failed loading sector page number: {sector_number}. Trying again...")
            attempt_number += 1


# Looping sectors sequentially
# for item in sectors.items():
#     sector_number = item[0]
#     sector_link = item[1]
#
#     print(f'Sector number: {sector_number}, sector link: {sector_link}')
#
#     attempt_number = 0
#     while attempt_number < max_attempt:
#         try:
#             response = html_loader.load_page(sector_link)
#             html = response.text
#             file_name = f'sector_{sector_number}_p1.html'
#             with open(file_name, 'a') as html_file:
#                 html_file.write(html)
#             print(f"Successfully loaded sector page number {sector_number} and saved to file {file_name}")
#
#             pages_count = cian_parser.get_pages_count(html)
#             print(f"Sector number {sector_number} has {pages_count} pages")
#             for i in range(2, pages_count+1):
#                 page_link = cian_parser.get_page_link(sector_link, i)
#                 print("-"*30)
#                 print(f"Loading page number: {i}")
#
#             sleep_seconds = random.randint(4, 6)
#             print(f'Sleeping for {sleep_seconds} seconds randomly')
#             time.sleep(sleep_seconds)
#
#             attempt_number = max_attempt
#         except Exception as exc:
#             print(f'Error: {exc}')
#             print(f"Failed loading sector page number: {sector_number}. Trying again...")
#             attempt_number += 1
