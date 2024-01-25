import unittest

from loaders.sector_list_loader import SectorListLoader


class TestLoadingSectorListCase(unittest.TestCase):
    def test_load_sector_list_from_google_sheet(self):
        test_sectors_url = "https://docs.google.com/spreadsheets/d/10egVpV2wRPsEtVvWVmqncP0cSwFu2tvdickJkBdGbBI"
        sheets_id = test_sectors_url[39:]
        credentials_file = '../tests/test_data/google_creds.json'

        sl = SectorListLoader()
        sectors = sl.load_sectors(sheets_id, credentials_file)

        self.assertEqual(4, len(sectors), "Wrong sectors count")
        self.assertEqual(True, '1' in sectors.keys(), "Sector #1 is not in the list")
        self.assertEqual(True, '2' in sectors.keys())
        self.assertEqual(True, '3' in sectors.keys())
        self.assertEqual(True, '12' in sectors.keys())

        self.assertEqual(True, "http://link1.ru/1" in sectors.values())
        self.assertEqual(True, "http://link2.ru/2" in sectors.values())
        self.assertEqual(True, "https://link3.ru/3" in sectors.values())
        self.assertEqual(True, "http://link12.com/12" in sectors.values())

    def test_load_production_sector_list(self):
        test_sectors_url = "https://docs.google.com/spreadsheets/d/1ph9a4sfNmwIEZKbWGwLX5iDYnOx6B5qdHYtuyIFR7H4"
        sheets_id = test_sectors_url[39:]
        credentials_file = '../tests/test_data/google_creds.json'

        sl = SectorListLoader()
        sectors = sl.load_sectors(sheets_id, credentials_file)

        self.assertLess(0, len(sectors), "Wrong sectors count")


if __name__ == '__main__':
    unittest.main()
