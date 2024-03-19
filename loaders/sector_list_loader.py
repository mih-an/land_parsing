import csv

class SectorListLoader:

    def __init__(self):
        self.credentials_file = None
        self.spreadsheet_id = None

    @staticmethod
    def load_sectors_from_cvs(sectors_cvs_file):
        with open(sectors_cvs_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            sector_list = {}
            for row in csv_reader:
                sector_number = row[0]
                sector_link = row[1]
                sector_list[sector_number] = sector_link

        return sector_list
