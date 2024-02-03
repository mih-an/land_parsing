import unittest

from html_readers.cian_parcer import CianParser


class TestCianParser(unittest.TestCase):
    def test_page_count_13(self):
        with open('cian_pages/cian_sector_17.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        pages_count = cian_parser.get_pages_count(test_html)

        self.assertEqual(13, pages_count, "Wrong pages count:")

    def test_page_count_21(self):
        with open('cian_pages/cian_sector_31.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        pages_count = cian_parser.get_pages_count(test_html)

        self.assertEqual(21, pages_count, "Wrong pages count:")

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
        self.assertEqual(1, pages_count)

    def test_link_for_page_2(self):
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

    def test_link_for_page_5(self):
        # Getting sector base link
        sector_base_link = ("https://www.cian.ru/cat.php?bbox=55.8563010218%2C36.4123966742%2C56.029898671%2C36"
                            ".7255070258&deal_type=sale&engine_version=2&in_polygon%5B1%5D=36.4930775_55.9640775%2C36"
                            ".4954808_55.9690869%2C36.4996006_55.9733256%2C36.5047505_55.9769863%2C36.5099003_55"
                            ".981225%2C36.5164235_55.984115%2C36.5236332_55.9866197%2C36.531873_55.9854637%2C36"
                            ".5394261_55.9833443%2C36.5469792_55.9814176%2C36.5548756_55.980069%2C36.562772_55"
                            ".9785276%2C36.5689518_55.9754449%2C36.5741017_55.9717842%2C36.5802815_55.9685089%2C36"
                            ".5878346_55.9663895%2C36.5940144_55.9631142%2C36.5981343_55.9590682%2C36.6036274_55"
                            ".9548295%2C36.6101506_55.9515541%2C36.617017_55.9486641%2C36.6242268_55.9453887%2C36"
                            ".6314366_55.942306%2C36.6379597_55.939416%2C36.6455128_55.9367187%2C36.6506627_55.933058"
                            "%2C36.6496327_55.928434%2C36.6451695_55.9243879%2C36.6389897_55.9211126%2C36.6324666_55"
                            ".9182225%2C36.6252568_55.9155252%2C36.6183903_55.9126352%2C36.6122105_55.9095525%2C36"
                            ".6060307_55.9060845%2C36.5995076_55.9031944%2C36.5919545_55.9006898%2C36.5833714_55"
                            ".8997264%2C36.5761616_55.9022311%2C36.5692952_55.9055065%2C36.562772_55.9085891%2C36"
                            ".5565922_55.9116718%2C36.5500691_55.9151399%2C36.5442326_55.9184152%2C36.5373661_55"
                            ".9218832%2C36.5311863_55.9255439%2C36.5246632_55.929012%2C36.5188267_55.9322873%2C36"
                            ".5129902_55.935948%2C36.5071537_55.9392234%2C36.5002873_55.9421134%2C36.4937642_55"
                            ".9453887%2C36.4889576_55.9494348%2C36.487241_55.9542515%2C36.487241_55.9590682%2C36"
                            ".488271_55.9636922%2C36.4930775_55.9640775&land_status%5B0%5D=1&land_status%5B1%5D=2"
                            "&land_status%5B2%5D=5&land_status%5B3%5D=7&maxsite=250&object_type%5B0%5D=3&offer_type"
                            "=suburban&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0"
                            "%B8%D1%81%D0%BA%D0%B0")
        test_link_page_5 = ("https://www.cian.ru/cat.php?bbox=55.8563010218%2C36.4123966742%2C56.029898671%2C36"
                            ".7255070258&deal_type=sale&engine_version=2&in_polygon%5B1%5D=36.4930775_55.9640775%2C36"
                            ".4954808_55.9690869%2C36.4996006_55.9733256%2C36.5047505_55.9769863%2C36.5099003_55"
                            ".981225%2C36.5164235_55.984115%2C36.5236332_55.9866197%2C36.531873_55.9854637%2C36"
                            ".5394261_55.9833443%2C36.5469792_55.9814176%2C36.5548756_55.980069%2C36.562772_55"
                            ".9785276%2C36.5689518_55.9754449%2C36.5741017_55.9717842%2C36.5802815_55.9685089%2C36"
                            ".5878346_55.9663895%2C36.5940144_55.9631142%2C36.5981343_55.9590682%2C36.6036274_55"
                            ".9548295%2C36.6101506_55.9515541%2C36.617017_55.9486641%2C36.6242268_55.9453887%2C36"
                            ".6314366_55.942306%2C36.6379597_55.939416%2C36.6455128_55.9367187%2C36.6506627_55.933058"
                            "%2C36.6496327_55.928434%2C36.6451695_55.9243879%2C36.6389897_55.9211126%2C36.6324666_55"
                            ".9182225%2C36.6252568_55.9155252%2C36.6183903_55.9126352%2C36.6122105_55.9095525%2C36"
                            ".6060307_55.9060845%2C36.5995076_55.9031944%2C36.5919545_55.9006898%2C36.5833714_55"
                            ".8997264%2C36.5761616_55.9022311%2C36.5692952_55.9055065%2C36.562772_55.9085891%2C36"
                            ".5565922_55.9116718%2C36.5500691_55.9151399%2C36.5442326_55.9184152%2C36.5373661_55"
                            ".9218832%2C36.5311863_55.9255439%2C36.5246632_55.929012%2C36.5188267_55.9322873%2C36"
                            ".5129902_55.935948%2C36.5071537_55.9392234%2C36.5002873_55.9421134%2C36.4937642_55"
                            ".9453887%2C36.4889576_55.9494348%2C36.487241_55.9542515%2C36.487241_55.9590682%2C36"
                            ".488271_55.9636922%2C36.4930775_55.9640775&land_status%5B0%5D=1&land_status%5B1%5D=2"
                            "&land_status%5B2%5D=5&land_status%5B3%5D=7&maxsite=250&object_type%5B0%5D=3&offer_type"
                            "=suburban&p=5&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0"
                            "%BE%D0%B8%D1%81%D0%BA%D0%B0")

        # Creating link with pages from base link and page number
        page_number = 5
        cian_parser = CianParser()
        sector_link_page_5 = cian_parser.get_page_link(sector_base_link, page_number)

        self.assertEqual(sector_link_page_5, test_link_page_5, "Page 5 link is incorrect")


if __name__ == '__main__':
    unittest.main()
