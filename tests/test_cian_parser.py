import unittest
import uuid

from db.ads_database import AdsDataBase
from html_readers.cian_parser import CianParser, ParseHelper

test_description1 = """Продаётся
 участок 9,9 соток в КП Майские Дачи.
* Поселок закрытый, участки граничат с лесом, имеют выход к реке.
* Категория земель: Земли сельскохозяйственного назначения.
* Разрешенное использование: Для дачного строительства.
* Участок пятиугольный, имеет удобное расположение, есть возможность 
организации двух заездов.
По всем вопросам звоните! 
----------------
* ДЛЯ ПОКУПАТЕЛЯ ОТ КОМПАНИИ ЭТАЖИ: 
- содействие в получении положительного решения по одобрению ипотеки в 
27 банках-партнёрах со сниженной процентной ставкой (преференцией) в 11 
банках (консультация бесплатно); 
- страхование объекта недвижимости со скидкой 25-30%; 
- юридическое сопровождение сделки; 
- безопасные расчёты; 
- финансовая гарантия на приобретаемый объект недвижимости до 15 млн. 
руб., в том числе до 1 млн. руб. по выплаченным % по ипотеке; 
- бесплатная консультация. 
Звоните! Оперативный показ.. Номер в базе: 8677442."""
test_description2 = """Продается
 участок в КП Прилесные дачи  6 сот. Прилесные дачи - это уникальный 
коттеджный поселок, комфорт класса, расположенный на берегу реки 
"Здеришка", с собственным выходом на береговую линию, в окружении 
смешанного леса. Уникальность поселка в его стоимости. Участки от 50 000
 рублей за сотку."""
test_description3 = """Широкие
 каналы со спокойно струящейся прозрачной водой, античные статуи вдоль 
тенистых дорожек в зелёных зарослях, тысячи солнечных зайчиков на 
зеркалах озёр  так выглядит "Миллениум Парк", элитный посёлок в 19 км от
 МКАД, давно ставший культовым. Именно здесь продается загородный 
участок ID 6032, уютный уголок для вашей будущей усадьбы. Кроме зелени и
 свежести от воды, поселение окутывает флёр спокойствия и безопасности. 
Сквозь заслон деревьев не проникает шум с автотрассы, лежащей в 1,5 км: к
 услугам жителей вся статусная инфраструктура Новой Риги. Четыре КПП 
позволяют удобно возвращаться домой с любой стороны, а вот для 
посторонних территория закрыта наглухо, без пропуска в посёлок не 
въехать. Что нужно знать о землевладении: площадь участка 14,41 сотки, 
коммуникации в готовности, в двух шагах детская площадка с игровыми 
аттракционами. Как купить недвижимость премиум-сегмента в рассрочку или 
взять в ипотеку, подскажут менеджеры Villagio Realty.

Номер лота: 6032"""
description6 = """Продаётся ПРИЛЕСНОЙ земельный участок 15 соток, 

Кадастровый номер 50:08:0070234:1228

Участок в закрытом, охраняемом коттеджном посёлке на 160 домовладений, 44 км от МКАД, 
1 час от Москва-Сити."""


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

    def test_number_from_text(self):
        title = "Купить земельный участок - 1 040 объявлений"
        cian_parser = CianParser()
        ads_count = cian_parser.get_number_from_str(title)
        self.assertEqual(1040, ads_count)

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

    def test_ads_count_sector17_p1(self):
        with open('cian_pages/cian_sector_17.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list = cian_parser.get_raw_ads(test_html)
        self.assertEqual(28, len(ads_list), "Wrong ads count:")

    def test_ads_count_sector1_p1(self):
        with open('cian_pages/cian_sector1.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list = cian_parser.get_raw_ads(test_html)
        self.assertEqual(19, len(ads_list), "Wrong ads count:")

    def test_sector17_ads1(self):
        with open('cian_pages/cian_sector_17.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)
        ads1 = ads_list[0]

        self.assertEqual('Участок, 9.9 сот., Садоводство', ads1.title, 'Title 1 is not correct')
        self.assertEqual(9.9, ads1.square, 'Square 1 is not correct')
        self.assertEqual(1800000, ads1.price, 'Price 1 is not correct')
        self.assertEqual('Садоводство', ads1.vri, 'VRI 1 is not correct')
        self.assertEqual('https://istra.cian.ru/sale/suburban/281048577/', ads1.link, 'Link 1 is not correct')
        self.assertEqual('281048577', ads1.id, 'Id 1 is not correct')
        self.assertEqual('', ads1.kp, 'Kp 1 is not correct')
        self.assertEqual('Московская область, Истра городской округ, Майские Дачи кп', ads1.address,
                         'Address 1 is not correct')
        self.assertEqual(test_description1, ads1.description, 'Description 1 is not correct')

    def test_sector17_ads2(self):
        with open('cian_pages/cian_sector_17.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)
        ads1 = ads_list[1]

        self.assertEqual('Участок, 6 сот.', ads1.title, 'Title 2 is not correct')
        self.assertEqual(6, ads1.square, 'Square 2 is not correct')
        self.assertEqual(425000, ads1.price, 'Price 2 is not correct')
        self.assertEqual('', ads1.vri, 'VRI 2 is not correct')
        self.assertEqual('https://istra.cian.ru/sale/suburban/287210218/', ads1.link, 'Link 2 is not correct')
        self.assertEqual('287210218', ads1.id, 'Id 2 is not correct')
        self.assertEqual('КП «‎Прилесные дачи »', ads1.kp, 'Kp 2 is not correct')
        self.assertEqual('Московская область, Истра городской округ, д. Малое Ушаково', ads1.address,
                         'Address 2 is not correct')
        self.assertEqual(test_description2, ads1.description, 'Description 2 is not correct')

    def test_sector17_ads3(self):
        with open('cian_pages/cian_sector_17.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)
        ads = ads_list[2]

        self.assertEqual('Участок, 12.5 сот., ДНП', ads.title, 'Title 3 is not correct')
        self.assertEqual(12.5, ads.square, 'Square 3 is not correct')
        self.assertEqual(4500000, ads.price, 'Price 3 is not correct')
        self.assertEqual('ДНП', ads.vri, 'VRI 3 is not correct')
        self.assertEqual('https://istra.cian.ru/sale/suburban/262375318/', ads.link, 'Link 3 is not correct')
        self.assertEqual('262375318', ads.id, 'Id 3 is not correct')
        self.assertEqual('', ads.kp, 'Kp 2 is not correct')
        self.assertEqual('Московская область, Истра городской округ, Озерный Край-2 кп', ads.address,
                         'Address 3 is not correct')

    def test_sector53(self):
        with open('cian_pages/cian_53.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)
        ads = ads_list[9]

        self.assertEqual('Участок, 5 сот., Садоводство', ads.title, 'Title 3 is not correct')
        self.assertEqual(5, ads.square, 'Square 3 is not correct')
        self.assertEqual(6000000, ads.price, 'Price 3 is not correct')
        self.assertEqual('Садоводство', ads.vri, 'VRI 3 is not correct')
        self.assertEqual('https://ivanteyevka.cian.ru/sale/suburban/298427227/', ads.link, 'Link 3 is not correct')

    def test_ads_owner(self):
        with open('cian_pages/cian_sector_17.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)

        ads = ads_list[0]
        self.assertEqual('Агентство недвижимости', ads.ads_owner, 'ads 1 owner is not correct')
        self.assertEqual('Этажи Москва', ads.ads_owner_id, 'ads 1 owner ID is not correct')

        ads = ads_list[2]
        self.assertEqual('Собственник', ads.ads_owner, 'ads 3 owner is not correct')
        self.assertEqual('ID 70642111', ads.ads_owner_id, 'ads 3 owner ID is not correct')

        ads = ads_list[3]
        self.assertEqual('Риелтор', ads.ads_owner, 'ads 4 owner is not correct')
        self.assertEqual('ID 23674176', ads.ads_owner_id, 'ads 4 owner ID is not correct')

        ads = ads_list[4]
        self.assertEqual('Застройщик', ads.ads_owner, 'ads 5 owner is not correct')
        self.assertEqual('Истринская Долина', ads.ads_owner_id, 'ads 5 owner ID is not correct')

    #     https://korolev.cian.ru/sale/suburban/283592675/
    # todo не распарсился Риэлтор (сектор 52)
    # АВТОР ОБЪЯВЛЕНИЯ https://ivanteyevka.cian.ru/sale/suburban/298863196/ (сектор 56)

    def test_electronic_trading(self):
        with open('cian_pages/cian_sector_17.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)

        ads = ads_list[0]
        self.assertEqual('', ads.electronic_trading, 'Electronic trading should not be')
        self.assertFalse(ads.is_electronic_trading, 'Electronic trading should be False ')

        ads = ads_list[9]
        self.assertEqual('Электронные торги', ads.electronic_trading, 'Electronic trading should be')
        self.assertTrue(ads.is_electronic_trading, 'Electronic trading should be True ')

        ads = ads_list[10]
        self.assertEqual('', ads.electronic_trading, 'Electronic trading should not be')
        self.assertFalse(ads.is_electronic_trading, 'Electronic trading should be False ')

        ads = ads_list[12]
        self.assertEqual('Электронные торги', ads.electronic_trading, 'Electronic trading should be')
        self.assertTrue(ads.is_electronic_trading, 'Electronic trading should be True ')

    def test_sector_31(self):
        with open('cian_pages/cian_sector_31.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)
        ads1 = ads_list[0]

        self.assertEqual('Участок, 14.41 сот.', ads1.title, 'Title 1 is not correct')
        self.assertEqual(14.41, ads1.square, 'Square 1 is not correct')
        self.assertEqual(66286000, ads1.price, 'Price 1 is not correct')
        self.assertEqual('', ads1.vri, 'VRI 1 is not correct')
        self.assertEqual('https://istra.cian.ru/sale/suburban/297552877/', ads1.link, 'Link 1 is not correct')
        self.assertEqual('297552877', ads1.id, 'Id 1 is not correct')
        self.assertEqual('КП «‎Millennium Park (Миллениум Парк)»', ads1.kp, 'Kp 1 is not correct')
        self.assertEqual('Московская область, Истра городской округ, Миллениум Парк кп, 8-011', ads1.address,
                         'Address 1 is not correct')

        ads = ads_list[6]
        self.assertEqual('Участок, 13.03 сот.', ads.title, 'Title 1 is not correct')
        self.assertEqual(13.03, ads.square, 'Square 1 is not correct')
        self.assertEqual(58635000, ads.price, 'Price 1 is not correct')

    def test_sector_29_addresses(self):
        with open('cian_pages/cian_sector_29.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)

        ads1 = ads_list[0]
        self.assertEqual('280878724', ads1.id, 'Id 1 is not correct')
        self.assertEqual('Московская область, Истра городской округ, д. Никулино, улица Овражная', ads1.address,
                         'Address is not correct')

        ads1 = ads_list[1]
        self.assertEqual('298558225', ads1.id, 'Id 1 is not correct')
        self.assertEqual('Московская область, Истра', ads1.address, 'Address is not correct')

        ads1 = ads_list[2]
        self.assertEqual('298501473', ads1.id, 'Id 1 is not correct')
        self.assertEqual(6, ads1.square, 'square is not correct')
        self.assertEqual('Московская область, Истра, улица 9-й Гвардейской Дивизии', ads1.address,
                         'Address is not correct')

        ads1 = ads_list[3]
        self.assertEqual('292750613', ads1.id, 'Id 1 is not correct')
        self.assertEqual('Московская область, Истра городской округ, пос. Северный', ads1.address,
                         'Address is not correct')

        ads1 = ads_list[7]
        self.assertEqual('296391361', ads1.id, 'Id 1 is not correct')
        self.assertEqual(200, ads1.square, 'square is not correct')
        self.assertEqual('Московская область, Истра, Южный мкр, улица Луговая', ads1.address,
                         'Address is not correct')

    def test_parce_square_from_title(self):
        parce_helper = ParseHelper()
        square = parce_helper.parse_square('Участок, 6 сот., Фермерское хозяйство')
        self.assertEqual(6, square)
        square = parce_helper.parse_square('Участок, 13.03 сот.')
        self.assertEqual(13.03, square)
        square = parce_helper.parse_square('Участок, 2 га, Садоводство')
        self.assertEqual(200, square)
        square = parce_helper.parse_square('Участок, 600 м², 6 сот., ИЖС')
        self.assertEqual(6, square)
        square = parce_helper.parse_square('Участок, 10 500 м², 1 га, ИЖС')
        self.assertEqual(105, square)

    def test_parce_kadastr_number(self):
        parce_helper = ParseHelper()

        description1 = 'профессиональной охраной.Кадастровый номер 50:09:0050704:823. Коммуникации по границе'
        kadastr_list = parce_helper.parse_kadastr(description1)
        self.assertEqual(1, len(kadastr_list))
        self.assertEqual('50:09:0050704:823', kadastr_list[0])

        description2 = 'Асфальт до участка. Кадастровый номер участка 50:08:0050314:836. Возможен торг'
        kadastr_list = parce_helper.parse_kadastr(description2)
        self.assertEqual(1, len(kadastr_list))
        self.assertEqual('50:08:0050314:836', kadastr_list[0])

        description3 = 'с документами всё идеально. Кадастровые номера: 50:08:0040153:75, 50:08:0040153:74'
        kadastr_list = parce_helper.parse_kadastr(description3)
        self.assertEqual(2, len(kadastr_list))
        self.assertEqual('50:08:0040153:75', kadastr_list[0])
        self.assertEqual('50:08:0040153:74', kadastr_list[1])

        description4 = 'с кадастровым номером 50:08:0040122:1043. Подключены'
        kadastr_list = parce_helper.parse_kadastr(description4)
        self.assertEqual(1, len(kadastr_list))
        self.assertEqual('50:08:0040122:1043', kadastr_list[0])

        description5 = 'район. Кадастровый номер  50:08:0040250:246. Участок '
        kadastr_list = parce_helper.parse_kadastr(description5)
        self.assertEqual(1, len(kadastr_list))
        self.assertEqual('50:08:0040250:246', kadastr_list[0])

        kadastr_list = parce_helper.parse_kadastr(description6)
        self.assertEqual(1, len(kadastr_list))
        self.assertEqual('50:08:0070234:1228', kadastr_list[0])

        description7 = 'из двух участков (50:08:0070234:1228; 50:08:0070234:1229) в закрытом'
        kadastr_list = parce_helper.parse_kadastr(description7)
        self.assertEqual(2, len(kadastr_list))
        self.assertEqual('50:08:0070234:1228', kadastr_list[0])
        self.assertEqual('50:08:0070234:1229', kadastr_list[1])

        description8 = 'номера участков с  50:08:0040229:1139 по  50:08:0040229:1165. Зе'
        kadastr_list = parce_helper.parse_kadastr(description8)
        self.assertEqual(2, len(kadastr_list))
        self.assertEqual('50:08:0040229:1139', kadastr_list[0])
        self.assertEqual('50:08:0040229:1165', kadastr_list[1])

        description9 = ('торгах до 23:59 24.02.2024 заявку с документами. Дата начала и дата торгов 04.03.2024 10:00 '
                        'по московскому времени. Звонить с 9:30 до 18:30 по м')
        kadastr_list = parce_helper.parse_kadastr(description9)
        self.assertEqual(0, len(kadastr_list))

        description10 = 'после 23:00 не нарушают'
        kadastr_list = parce_helper.parse_kadastr(description10)
        self.assertEqual(0, len(kadastr_list))

    def test_sector_26_p2_addresses(self):
        with open('cian_pages/sector_26_p2.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list, is_error = cian_parser.get_ads(test_html)

        ads1 = ads_list[0]
        self.assertEqual('298377384', ads1.id, 'Id 1 is not correct')
        self.assertEqual('Московская область, Истра городской округ, д. Леоново, 6', ads1.address,
                         'Address is not correct')

    def test_html_has_captcha(self):
        cian_parser = CianParser()

        with open('cian_pages/sector_4_p1.html', 'r') as test_html_file:
            test_html = test_html_file.read()
        has_captcha = cian_parser.has_captcha(test_html)
        self.assertTrue(has_captcha)

        with open('cian_pages/sector_26_p2.html', 'r') as test_html_file:
            test_html = test_html_file.read()
        has_captcha = cian_parser.has_captcha(test_html)
        self.assertFalse(has_captcha)

    def test_bug_out_of_range_price(self):
        with open('cian_pages/cian_31_21.html', 'r') as test_html_file:
            test_html = test_html_file.read()

        cian_parser = CianParser()
        ads_list = cian_parser.get_raw_ads(test_html)
        self.assertEqual(16, len(ads_list), "Wrong ads count:")

        ads_list, is_error = cian_parser.get_ads(test_html)
        self.assertFalse(is_error, "It should not have errors")
        self.assertEqual(16, len(ads_list), "Wrong ads count:")

        ads_db = AdsDataBase()
        for ads in ads_list:
            ads.sector_number = 1
            ads.id = str(uuid.uuid4())
            # Old date. Does not need to bother other test because it relies on creation date
            ads.first_parse_datetime = '2023-01-20 10:28:10'
            ads.last_parse_datetime = ads.first_parse_datetime
        ads_db.save(ads_list)


if __name__ == '__main__':
    unittest.main()
