import unittest

from loaders.link_helper import LinkHelper, Coordinate

test_link1 = ('https://www.cian.ru/cat.php?bbox=56.0997233901%2C36.7516463512%2C56.1797535595%2C37.0729964488'
              '&deal_type=sale&engine_version=2&in_polygon%5B1%5D=36.9126647_56.130252%2C36.9181579_56.1266055%2C36'
              '.9229644_56.1225752%2C36.9284576_56.1189287%2C36.935324_56.1162418%2C36.9435638_56.1160499%2C36'
              '.9514602_56.1175853%2C36.9518035_56.1223833%2C36.9524902_56.1269894%2C36.9511169_56.1315954%2C36'
              '.9483703_56.1362015%2C36.9494003_56.1409995%2C36.9452804_56.1450299%2C36.937384_56.1473329%2C36'
              '.9288009_56.149444%2C36.9222778_56.1527067%2C36.9164413_56.1561612%2C36.9088882_56.1580804%2C36'
              '.9009918_56.1601916%2C36.8930953_56.1626865%2C36.8848556_56.1634542%2C36.881079_56.15904%2C36'
              '.8786758_56.1546259%2C36.8755859_56.1502117%2C36.8731826_56.1457975%2C36.8721526_56.1411914%2C36'
              '.8769592_56.1371611%2C36.8855422_56.1354338%2C36.8934387_56.1340904%2C36.9013351_56.132747%2C36'
              '.9085449_56.1304439%2C36.9126647_56.130252&maxsite=250&object_type%5B0%5D=3&offer_type=suburban'
              '&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0')
test_link2 = ('https://www.cian.ru/cat.php/?center=55.806737048576515%2C36.995401242747896&deal_type=sale'
              '&engine_version=2&in_polygon%5B1%5D=37.075899_55.7852039%2C37.0717792_55.7853006%2C37.067831_55'
              '.7859776%2C37.0633678_55.7869448%2C37.0601062_55.7884923%2C37.0573596_55.7903299%2C37.054613_55'
              '.7925544%2C37.0515231_55.7944887%2C37.0491199_55.796423%2C37.0465449_55.7983573%2C37.0441417_55'
              '.8007753%2C37.0417384_55.802903%2C37.0388202_55.8049341%2C37.0360736_55.806675%2C37.033327_55.8085126'
              '%2C37.0307521_55.8108338%2C37.0269756_55.8125747%2C37.0238856_55.8142188%2C37.022169_55.8163466%2C37'
              '.0183925_55.8177006%2C37.0142726_55.8183776%2C37.0101527_55.8186678%2C37.0056895_55.8188612%2C37'
              '.0012263_55.8190547%2C36.9969348_55.8192481%2C36.9926433_55.8194415%2C36.9883517_55.8194415%2C36'
              '.9837169_55.8193448%2C36.979597_55.8189579%2C36.9751338_55.8188612%2C36.9706706_55.8188612%2C36'
              '.9665507_55.8189579%2C36.9622592_55.8188612%2C36.9584827_55.8177974%2C36.9553928_55.8162499%2C36'
              '.9531612_55.8140254%2C36.9516162_55.8117042%2C36.9509296_55.8092863%2C36.9502429_55.8069651%2C36'
              '.9502429_55.8045472%2C36.9500713_55.802226%2C36.9505862_55.7999048%2C36.9511012_55.7970033%2C36'
              '.9511012_55.794392%2C36.9507579_55.7919741%2C36.9512729_55.7894594%2C36.9535045_55.7868481%2C36'
              '.9550494_55.7844302%2C36.9571094_55.7822057%2C36.9603709_55.7803681%2C36.9638042_55.7789173%2C36'
              '.9674091_55.7777567%2C36.9717006_55.7771764%2C36.9758205_55.7772732%2C36.9802837_55.7777567%2C36'
              '.9845752_55.77766%2C36.9888667_55.7771764%2C36.9933299_55.7764027%2C36.9972781_55.7753388%2C37'
              '.0031146_55.7734045%2C37.0075778_55.7717603%2C37.0111827_55.7703096%2C37.0149593_55.7687621%2C37'
              '.0185641_55.7676015%2C37.0223407_55.7666344%2C37.0262889_55.7655705%2C37.0302371_55.7647%2C37'
              '.0345287_55.7642164%2C37.0393352_55.7642164%2C37.0437984_55.7647%2C37.0474033_55.7660541%2C37'
              '.0504932_55.7676982%2C37.0534114_55.7694391%2C37.0563296_55.77118%2C37.0592479_55.7728242%2C37'
              '.0628528_55.7747585%2C37.0661143_55.7766929%2C37.0690326_55.7787239%2C37.0716075_55.7805615%2C37'
              '.0743541_55.7824958%2C37.0757274_55.7847203%2C37.075899_55.7852039&maxsite=252&object_type%5B0%5D=3'
              '&offer_type=suburban&polygon_name%5B0%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%20%D0%BF%D0%BE%D0'
              '%B8%D1%81%D0%BA%D0%B0')


class TestUniqueLinks(unittest.TestCase):
    def test_reading_raw_coordinates(self):
        link_helper = LinkHelper()
        coord_list = link_helper.read_raw_coordinates(test_link1)
        self.assertEqual(32, len(coord_list), 'Coordinates count isn\'t correct')
        self.assertEqual('36.9126647_56.130252', coord_list[0], 'Coordinate 1 isn\'t correct')
        self.assertEqual('36.9181579_56.1266055', coord_list[1], 'Coordinate 2 isn\'t correct')
        self.assertEqual('36.9229644_56.1225752', coord_list[2], 'Coordinate 3 isn\'t correct')
        self.assertEqual('36.9085449_56.1304439', coord_list[30], 'Coordinate 31 isn\'t correct')
        self.assertEqual('36.9126647_56.130252', coord_list[31], 'Coordinate 32 isn\'t correct')

    def test_reading_coordinates(self):
        link_helper = LinkHelper()
        coord_list = link_helper.read_coordinates(test_link2)
        self.assertEqual(82, len(coord_list), 'Coordinates count isn\'t correct')
        self.assertEqual('37.075899', coord_list[0].longitude, 'Coordinate 1 longitude isn\'t correct')
        self.assertEqual('55.7852039', coord_list[0].latitude, 'Coordinate 1 latitude isn\'t correct')
        self.assertEqual('37.0717792', coord_list[1].longitude, 'Coordinate 2 longitude isn\'t correct')
        self.assertEqual('55.7853006', coord_list[1].latitude, 'Coordinate 2 latitude isn\'t correct')
        self.assertEqual('37.0757274', coord_list[80].longitude, 'Coordinate 81 longitude isn\'t correct')
        self.assertEqual('55.7847203', coord_list[80].latitude, 'Coordinate 81 latitude isn\'t correct')
        self.assertEqual('37.075899', coord_list[81].longitude, 'Coordinate 82 longitude isn\'t correct')
        self.assertEqual('55.7852039', coord_list[81].latitude, 'Coordinate 82 latitude isn\'t correct')

    def test_reading_raw_bbox(self):
        link_helper = LinkHelper()
        bbox_raw = link_helper.read_raw_bbox(test_link1)
        self.assertEqual('56.0997233901%2C36.7516463512%2C56.1797535595%2C37.0729964488',
                         bbox_raw, 'Bbox 1 isn\'t correct')
        bbox_raw = link_helper.read_raw_bbox(test_link2)
        self.assertEqual('', bbox_raw, 'Bbox 2 isn\'t correct')

    def test_reading_bbox(self):
        link_helper = LinkHelper()
        bbox_coord_list = link_helper.read_bbox(test_link1)

        self.assertEqual(2, len(bbox_coord_list), 'Bbox 1 list length isn\'t correct')
        self.assertEqual('36.7516463512', bbox_coord_list[0].longitude, 'Bbox coordinate 1 longitude isn\'t correct')
        self.assertEqual('56.0997233901', bbox_coord_list[0].latitude, 'Bbox coordinate 1 latitude isn\'t correct')
        self.assertEqual('37.0729964488', bbox_coord_list[1].longitude, 'Bbox coordinate 2 longitude isn\'t correct')
        self.assertEqual('56.1797535595', bbox_coord_list[1].latitude, 'Bbox coordinate 2 latitude isn\'t correct')

        bbox_coord_list = link_helper.read_bbox(test_link2)
        self.assertEqual(0, len(bbox_coord_list), 'Bbox 2 list length isn\'t correct')

    def test_reading_center(self):
        link_helper = LinkHelper()
        center = link_helper.read_center(test_link1)
        self.assertIsNone(center, 'Center isn\'t None')

        center = link_helper.read_center(test_link2)
        self.assertIsNotNone(center, 'Center is None')
        self.assertEqual('36.995401242747896', center.longitude, 'Center 2 longitude isn\'t correct')
        self.assertEqual('55.806737048576515', center.latitude, 'Center 2 latitude isn\'t correct')

    def test_reading_maxsite(self):
        link_helper = LinkHelper()
        maxsite = link_helper.read_maxsite(test_link1)
        self.assertEqual('250', maxsite, 'Maxsite 1 isn\'t correct')
        maxsite = link_helper.read_maxsite(test_link2)
        self.assertEqual('252', maxsite, 'Maxsite 2 isn\'t correct')

    def test_changing_coordinates(self):
        lh = LinkHelper()
        coordinate = Coordinate(longitude='36.9126647', latitude='56.130252')
        new_coordinate = lh.gen_new_coordinate(coordinate)
        self.assertIsNotNone(new_coordinate)
        self.assertEqual(len(coordinate.longitude), len(new_coordinate.longitude), 'Longitude 1 length is not the same')
        self.assertEqual(len(coordinate.latitude), len(new_coordinate.latitude), 'Latitude 1 length is not the same')
        self.assertNotEqual(coordinate.longitude, new_coordinate.longitude, 'Longitude should not be the same')
        self.assertNotEqual(coordinate.latitude, new_coordinate.latitude, 'Latitude should not be the same')

        coordinate = Coordinate(longitude='36.995401242747896', latitude='55.806737048576515')
        new_coordinate = lh.gen_new_coordinate(coordinate)
        self.assertIsNotNone(new_coordinate)
        self.assertEqual(len(coordinate.longitude), len(new_coordinate.longitude), 'Longitude 2 length is not the same')
        self.assertEqual(len(coordinate.latitude), len(new_coordinate.latitude), 'Latitude 2 length is not the same')
        self.assertNotEqual(coordinate.longitude, new_coordinate.longitude, 'Longitude should not be the same')
        self.assertNotEqual(coordinate.latitude, new_coordinate.latitude, 'Latitude should not be the same')

    def test_first_4_coordinate_digits_still_the_same(self):
        lh = LinkHelper()
        coordinate = Coordinate(longitude='36.9126647', latitude='56.130252')
        new_coordinate = lh.gen_new_coordinate(coordinate)
        self.assertEqual(coordinate.latitude[:7], new_coordinate.latitude[:7])
        self.assertEqual(coordinate.longitude[:7], new_coordinate.longitude[:7])

        coordinate = Coordinate(longitude='36.995401242747896', latitude='55.806737048576515')
        new_coordinate = lh.gen_new_coordinate(coordinate)
        self.assertEqual(coordinate.latitude[:7], new_coordinate.latitude[:7])
        self.assertEqual(coordinate.longitude[:7], new_coordinate.longitude[:7])

    def test_count_and_order_of_coordinates(self):
        lh = LinkHelper()
        new_coord_list = lh.gen_new_coordinates(test_link1)
        self.assertEqual(32, len(new_coord_list))
        self.assertEqual('36.9126', new_coord_list[0].longitude[:7], 'Coordinate 1 isn\'t correct')
        self.assertEqual('56.1302', new_coord_list[0].latitude[:7], 'Coordinate 1 isn\'t correct')
        self.assertEqual('36.9181', new_coord_list[1].longitude[:7], 'Coordinate 2 isn\'t correct')
        self.assertEqual('56.1266', new_coord_list[1].latitude[:7], 'Coordinate 2 isn\'t correct')
        self.assertEqual('36.9229', new_coord_list[2].longitude[:7], 'Coordinate 3 isn\'t correct')
        self.assertEqual('56.1225', new_coord_list[2].latitude[:7], 'Coordinate 3 isn\'t correct')
        self.assertEqual('36.9085', new_coord_list[30].longitude[:7], 'Coordinate 31 isn\'t correct')
        self.assertEqual('56.1304', new_coord_list[30].latitude[:7], 'Coordinate 31 isn\'t correct')
        self.assertEqual('36.9126', new_coord_list[31].longitude[:7], 'Coordinate 32 isn\'t correct')
        self.assertEqual('56.1302', new_coord_list[31].latitude[:7], 'Coordinate 32 isn\'t correct')

        link_helper = LinkHelper()
        new_coord_list = link_helper.gen_new_coordinates(test_link2)
        self.assertEqual(82, len(new_coord_list), 'Coordinates count isn\'t correct')
        self.assertEqual('37.0758', new_coord_list[0].longitude[:7], 'Coordinate 1 longitude isn\'t correct')
        self.assertEqual('55.7852', new_coord_list[0].latitude[:7], 'Coordinate 1 latitude isn\'t correct')
        self.assertEqual('37.0717', new_coord_list[1].longitude[:7], 'Coordinate 2 longitude isn\'t correct')
        self.assertEqual('55.7853', new_coord_list[1].latitude[:7], 'Coordinate 2 latitude isn\'t correct')
        self.assertEqual('37.0757', new_coord_list[80].longitude[:7], 'Coordinate 81 longitude isn\'t correct')
        self.assertEqual('55.7847', new_coord_list[80].latitude[:7], 'Coordinate 81 latitude isn\'t correct')
        self.assertEqual('37.0758', new_coord_list[81].longitude[:7], 'Coordinate 82 longitude isn\'t correct')
        self.assertEqual('55.7852', new_coord_list[81].latitude[:7], 'Coordinate 82 latitude isn\'t correct')

    def test_maxsite_generation(self):
        link_helper = LinkHelper()
        new_maxsite_int = link_helper.gen_new_maxsite_int()
        self.assertGreater(271, new_maxsite_int, "Max site should be between 230 and 270")
        self.assertLess(229, new_maxsite_int, "Max site should be between 230 and 270")

    def test_bbox_to_link(self):
        link_helper = LinkHelper()
        coord_list = [Coordinate(longitude='36.7516463512', latitude='56.0997233901'),
                      Coordinate(longitude='37.0729964488', latitude='56.1797535595')]
        url_part = link_helper.bbox_to_url_str(coord_list)

        self.assertEqual('56.0997233901%2C36.7516463512%2C56.1797535595%2C37.0729964488', url_part,
                         'Bbox link is not correct')

    def test_bbox_modification(self):
        lh = LinkHelper()
        new_link = lh.gen_new_unique_url(test_link1)

        bbox_coord_list = lh.read_bbox(new_link)
        self.assertEqual(2, len(bbox_coord_list), 'Bbox 1 list length isn\'t correct')
        self.assertEqual('36.7516', bbox_coord_list[0].longitude[:7], 'Bbox coordinate 1 longitude isn\'t correct')
        self.assertEqual('56.0997', bbox_coord_list[0].latitude[:7], 'Bbox coordinate 1 latitude isn\'t correct')
        self.assertEqual('37.0729', bbox_coord_list[1].longitude[:7], 'Bbox coordinate 2 longitude isn\'t correct')
        self.assertEqual('56.1797', bbox_coord_list[1].latitude[:7], 'Bbox coordinate 2 latitude isn\'t correct')

        self.assertNotEqual('463512', bbox_coord_list[0].longitude[7:], 'Bbox coordinate 1 longitude isn\'t correct')
        self.assertNotEqual('233901', bbox_coord_list[0].latitude[7:], 'Bbox coordinate 1 latitude isn\'t correct')
        self.assertNotEqual('964488', bbox_coord_list[1].longitude[7:], 'Bbox coordinate 2 longitude isn\'t correct')
        self.assertNotEqual('535595', bbox_coord_list[1].latitude[7:], 'Bbox coordinate 2 latitude isn\'t correct')

        self.assertEqual(13, len(bbox_coord_list[0].longitude), 'Bbox coordinate 1 longitude length')
        self.assertEqual(13, len(bbox_coord_list[0].latitude), 'Bbox coordinate 1 latitude length')
        self.assertEqual(13, len(bbox_coord_list[1].longitude), 'Bbox coordinate 2 longitude length')
        self.assertEqual(13, len(bbox_coord_list[1].latitude), 'Bbox coordinate 2 latitude length')

        new_link = lh.gen_new_unique_url(test_link2)
        bbox_coord_list = lh.read_bbox(new_link)
        self.assertEqual(0, len(bbox_coord_list), 'Bbox 2 list length isn\'t correct')

    def test_center_to_link(self):
        lh = LinkHelper()
        center = Coordinate(longitude='36.995401242747896', latitude='55.806737048576515')
        url_part = lh.center_to_url_str(center)
        self.assertEqual('55.806737048576515%2C36.995401242747896', url_part, 'Center link is not correct')

    def test_center_modification(self):
        lh = LinkHelper()
        new_link = lh.gen_new_unique_url(test_link1)

        center = lh.read_center(new_link)
        self.assertIsNone(center, 'Center should be None in first link')

        new_link = lh.gen_new_unique_url(test_link2)
        center = lh.read_center(new_link)
        self.assertIsNotNone(center, 'Center should NOT be None in first link')
        # 55.806737048576515%2C36.995401242747896
        self.assertEqual('36.9954', center.longitude[:7], 'Center coordinate longitude isn\'t correct')
        self.assertEqual('55.8067', center.latitude[:7], 'Center coordinate latitude isn\'t correct')

        self.assertEqual('42747896', center.longitude[10:18], 'Center coordinate longitude isn\'t correct')
        self.assertEqual('48576515', center.latitude[10:18], 'Center coordinate latitude isn\'t correct')

        self.assertNotEqual('012', center.longitude[7:10], 'Center coordinate longitude isn\'t correct')
        self.assertNotEqual('370', center.latitude[7:10], 'Center coordinate latitude isn\'t correct')

        self.assertEqual(18, len(center.longitude), 'Bbox coordinate 1 longitude length')
        self.assertEqual(18, len(center.latitude), 'Bbox coordinate 1 latitude length')

    def test_maxsite_modification(self):
        lh = LinkHelper()
        new_link = lh.gen_new_unique_url(test_link1)

        maxsite = lh.read_maxsite(new_link)
        self.assertNotEqual('250', maxsite, 'Maxsite should be new')
        maxsite_int = int(maxsite)
        self.assertGreater(271, maxsite_int, "Max site should be between 230 and 270")
        self.assertLess(229, maxsite_int, "Max site should be between 230 and 270")

    def test_coordinates_to_link(self):
        link_helper = LinkHelper()
        coord_list = [Coordinate(longitude='36.9126647', latitude='56.130252'),
                      Coordinate(longitude='36.995401242747896', latitude='55.806737048576515'),
                      Coordinate(longitude='36.123', latitude='55.76543299')]
        url_part = link_helper.coordinates_to_url_str(coord_list)

        self.assertEqual('36.9126647_56.130252%2C36.995401242747896_55.806737048576515%2C36.123_55.76543299',
                         url_part, 'Link is not correct')

    def test_new_link2_coordinates(self):
        link_helper = LinkHelper()
        new_link = link_helper.gen_new_unique_url(test_link2)

        self.assertEqual(len(test_link2), len(new_link))
        self.assertNotEqual(test_link2, new_link)

        base_coord_list = link_helper.read_coordinates(test_link2)
        new_coord_list = link_helper.read_coordinates(new_link)

        self.assertEqual(len(base_coord_list), len(new_coord_list), 'Coordinates count isn\'t correct')
        self.assertEqual(base_coord_list[0].longitude[:7], new_coord_list[0].longitude[:7],
                         'Coordinate 1 longitude isn\'t correct')
        self.assertEqual(base_coord_list[0].latitude[:7], new_coord_list[0].latitude[:7],
                         'Coordinate 1 latitude isn\'t correct')
        self.assertEqual(base_coord_list[1].longitude[:7], new_coord_list[1].longitude[:7],
                         'Coordinate 2 longitude isn\'t correct')
        self.assertEqual(base_coord_list[1].latitude[:7], new_coord_list[1].latitude[:7],
                         'Coordinate 2 latitude isn\'t correct')
        self.assertEqual(base_coord_list[80].longitude[:7], new_coord_list[80].longitude[:7],
                         'Coordinate 80 longitude isn\'t correct')
        self.assertEqual(base_coord_list[80].latitude[:7], new_coord_list[80].latitude[:7],
                         'Coordinate 80 latitude isn\'t correct')
        self.assertEqual(base_coord_list[81].longitude[:7], new_coord_list[81].longitude[:7],
                         'Coordinate 81 longitude isn\'t correct')
        self.assertEqual(base_coord_list[81].latitude[:7], new_coord_list[81].latitude[:7],
                         'Coordinate 81 latitude isn\'t correct')

    def test_new_link1_coordinates(self):
        link_helper = LinkHelper()
        new_link = link_helper.gen_new_unique_url(test_link1)

        self.assertEqual(len(test_link1), len(new_link))
        self.assertNotEqual(test_link1, new_link)

        base_coord_list = link_helper.read_coordinates(test_link1)
        new_coord_list = link_helper.read_coordinates(new_link)

        self.assertEqual(len(base_coord_list), len(new_coord_list), 'Coordinates count isn\'t correct')
        self.assertEqual(base_coord_list[0].longitude[:7], new_coord_list[0].longitude[:7],
                         'Coordinate 1 longitude isn\'t correct')
        self.assertEqual(base_coord_list[0].latitude[:7], new_coord_list[0].latitude[:7],
                         'Coordinate 1 latitude isn\'t correct')
        self.assertEqual(base_coord_list[1].longitude[:7], new_coord_list[1].longitude[:7],
                         'Coordinate 2 longitude isn\'t correct')
        self.assertEqual(base_coord_list[1].latitude[:7], new_coord_list[1].latitude[:7],
                         'Coordinate 2 latitude isn\'t correct')
        self.assertEqual(base_coord_list[30].longitude[:7], new_coord_list[30].longitude[:7],
                         'Coordinate 30 longitude isn\'t correct')
        self.assertEqual(base_coord_list[30].latitude[:7], new_coord_list[30].latitude[:7],
                         'Coordinate 30 latitude isn\'t correct')
        self.assertEqual(base_coord_list[31].longitude[:7], new_coord_list[31].longitude[:7],
                         'Coordinate 31 longitude isn\'t correct')
        self.assertEqual(base_coord_list[31].latitude[:7], new_coord_list[31].latitude[:7],
                         'Coordinate 31 latitude isn\'t correct')

    def test_first_coord_equals_last_coordinate(self):
        lh = LinkHelper()

        new_coord_list = lh.gen_new_coordinates(test_link1)
        self.assertEqual(new_coord_list[0].longitude, new_coord_list[31].longitude,
                         'First and last longitude should be the same')
        self.assertEqual(new_coord_list[0].latitude, new_coord_list[31].latitude,
                         'First and last latitude should be the same')

        new_link = lh.gen_new_unique_url(test_link1)
        new_coord_list = lh.read_coordinates(new_link)
        self.assertEqual(new_coord_list[31].latitude, new_coord_list[0].latitude,
                         'First and last latitude should be the same')
        self.assertEqual(new_coord_list[31].longitude, new_coord_list[0].longitude,
                         'First and last longitude should be the same')


if __name__ == '__main__':
    unittest.main()
