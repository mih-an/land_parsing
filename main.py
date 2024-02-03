import time
import random
import creds
from datetime import datetime

from html_readers.cian_parcer import CianParser
from loaders.html_loader import HtmlLoader
from loaders.link_helper import LinkHelper
from loaders.sector_list_loader import SectorListLoader

test_sectors_url = "https://docs.google.com/spreadsheets/d/1ph9a4sfNmwIEZKbWGwLX5iDYnOx6B5qdHYtuyIFR7H4"
sheets_id = test_sectors_url[39:]
credentials_file = 'tests/test_data/google_creds.json'

sector_loader = SectorListLoader()
sectors = sector_loader.load_sectors(sheets_id, credentials_file)

max_attempt = 3

proxies = {
    'http': f'{creds.login}:{creds.password}@{creds.ip}'
}

cian_parser = CianParser()
html_loader = HtmlLoader()
html_loader.set_proxies(proxies)
link_helper = LinkHelper()

# Looping all sectors randomly
sectors_copy = sectors.copy()
while len(sectors_copy) > 0:
    print('='*100)
    print(f'Sectors left to download: {len(sectors_copy)}')
    sector_number = random.choice(list(sectors_copy.keys()))
    sector_link = sectors_copy[sector_number]
    print(f'Sector number: {sector_number}, sector link: {sector_link}')

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    attempt_number = 0
    while attempt_number < max_attempt:
        try:
            sector_link = link_helper.gen_new_url(sector_link)
            print(f'Loading sector link... {sector_link}')
            response = html_loader.load_page(sector_link)
            html = response.text
            file_name = f'sector_{sector_number}_p1.html'
            with open(file_name, 'a') as html_file:
                html_file.write(html)
            print(f"Sector loaded successfully and saved to the file: {file_name}")

            sleep_seconds = random.randint(5, 7)
            print(f'Sleeping for {sleep_seconds} seconds...')
            time.sleep(sleep_seconds)

            attempt_number = max_attempt
            del sectors_copy[sector_number]

            pages_count = cian_parser.get_pages_count(html)
            print(f"Sector number {sector_number} has {pages_count} pages")
            for i in range(2, pages_count + 1):
                print("-" * 30)
                print(f"Loading page number: {i}...")

                # # TODO сделать несколько попыток загрузки страницы, а то сейчас страницы начинают грузиться заново
                # page_link = cian_parser.get_page_link(sector_link, i)
                # response = html_loader.load_page(page_link)
                # file_name = f'sector_{sector_number}_p{i}.html'
                # with open(file_name, 'a') as html_file:
                #     html_file.write(html)
                # print(f"Sector loaded successfully and saved to the file: {file_name}")
                #
                # # Excluding 2 sleeping in the last cycle
                # if i < pages_count:
                #     sleep_seconds = random.randint(4, 6)
                #     print(f'Sleeping for {sleep_seconds} seconds...')
                #     time.sleep(sleep_seconds)

        except Exception as exc:
            attempt_number += 1
            print(f"Failed loading sector number: {sector_number}. Trying again... Attempt № {attempt_number}")
            print(f'Error: {exc}')
            sleep_seconds = 10
            print(f'Sleeping for {sleep_seconds} seconds...')
            time.sleep(sleep_seconds)
