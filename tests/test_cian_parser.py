import unittest

from html_readers.cian_parcer import CianParser


class TestCianParser(unittest.TestCase):
    def test_pages_count_5(self):
        with open('cian_pages/cian_sector_21_p1.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        pages_count = cian_parser.get_pages_count(test_html)

        self.assertEqual(5, pages_count, "Wrong pages count:")

    def test_pages_count_2(self):
        with open('cian_pages/cian_sector_9_p1.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        pages_count = cian_parser.get_pages_count(test_html)

        self.assertEqual(2, pages_count, "Wrong pages count:")  # add assertion here

    def test_no_pagination(self):
        with open('cian_pages/cian_sector1.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        pages_count = cian_parser.get_pages_count(test_html)
        self.assertEqual(0, pages_count)

    def test_pages_links(self):
        # Getting sector base link
        sector_base_link = ("https://www.cian.ru/cat.php?bbox=56.0520810995%2C36.7602801621%2C56.1385371939%2C36"
                            ".9168353379&deal_type=sale&engine_version=2&in_polygon%5B1%5D=36.8172717_56.1161569%2C36"
                            ".8258548_56.1161569%2C36.8340945_56.1157729%2C36.8423343_56.115197%2C36.8509173_56"
                            ".1146211%2C36.8591571_56.1142371%2C36.8673968_56.1136612%2C36.8756366_56.1132773%2C36"
                            ".8838763_56.1123174%2C36.8921161_56.1109736%2C36.8955493_56.1067502%2C36.8955493_56"
                            ".1019508%2C36.8934894_56.0973435%2C36.8903995_56.0929281%2C36.8862796_56.0888966%2C36"
                            ".8849063_56.0842893%2C36.8821597_56.0798739%2C36.8776965_56.0758424%2C36.8698001_56"
                            ".0744986%2C36.8615604_56.0743067%2C36.8536639_56.0758424%2C36.8450809_56.0764184%2C36"
                            ".8368411_56.0775702%2C36.828258_56.0783381%2C36.8200183_56.078914%2C36.8110919_56.078914"
                            "%2C36.8025088_56.078722%2C36.7946124_56.0802578%2C36.7870593_56.0831374%2C36.7825961_56"
                            ".0873608%2C36.7815662_56.0919682%2C36.7829394_56.0965756%2C36.7870593_56.100607%2C36"
                            ".7915225_56.1046385%2C36.7949557_56.1090538%2C36.8004489_56.1128933%2C36.809032_56"
                            ".1140452%2C36.8162418_56.1163488%2C36.8172717_56.1161569&maxsite=250&object_type%5B0%5D"
                            "=3&offer_type=suburban&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C"
                            "+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0")
        test_link_page_2 = ("https://www.cian.ru/cat.php?bbox=56.0520810995%2C36.7602801621%2C56.1385371939%2C36"
                            ".9168353379&deal_type=sale&engine_version=2&in_polygon%5B1%5D=36.8172717_56.1161569"
                            "%2C36.8258548_56.1161569%2C36.8340945_56.1157729%2C36.8423343_56.115197%2C36"
                            ".8509173_56.1146211%2C36.8591571_56.1142371%2C36.8673968_56.1136612%2C36.8756366_56"
                            ".1132773%2C36.8838763_56.1123174%2C36.8921161_56.1109736%2C36.8955493_56.1067502%2C36"
                            ".8955493_56.1019508%2C36.8934894_56.0973435%2C36.8903995_56.0929281%2C36.8862796_56"
                            ".0888966%2C36.8849063_56.0842893%2C36.8821597_56.0798739%2C36.8776965_56.0758424%2C36"
                            ".8698001_56.0744986%2C36.8615604_56.0743067%2C36.8536639_56.0758424%2C36.8450809_56"
                            ".0764184%2C36.8368411_56.0775702%2C36.828258_56.0783381%2C36.8200183_56.078914%2C36"
                            ".8110919_56.078914%2C36.8025088_56.078722%2C36.7946124_56.0802578%2C36.7870593_56"
                            ".0831374%2C36.7825961_56.0873608%2C36.7815662_56.0919682%2C36.7829394_56.0965756%2C36"
                            ".7870593_56.100607%2C36.7915225_56.1046385%2C36.7949557_56.1090538%2C36.8004489_56"
                            ".1128933%2C36.809032_56.1140452%2C36.8162418_56.1163488%2C36.8172717_56.1161569"
                            "&maxsite=250&object_type%5B0%5D=3&offer_type=suburban&p=2&polygon_name%5B1%5D=%D0%9E"
                            "%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0")

        # Creating link with pages from base link and page number
        page_number = 2
        cian_parser = CianParser()
        sector_link_page_2 = cian_parser.get_page_link(sector_base_link, page_number)

        self.assertEqual(sector_link_page_2, test_link_page_2, "Next page link is incorrect")

    def test_no_pagination_pages_links(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
