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
              '&engine_version=2&in_polygon%5B0%5D=37.075899_55.7852039%2C37.0717792_55.7853006%2C37.067831_55'
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
        link_list = link_helper.get_raw_coordinates(test_link1)
        self.assertEqual(32, len(link_list), 'Coordinates count isn\'t correct')
        self.assertEqual('36.9126647_56.130252', link_list[0], 'Coordinate 1 isn\'t correct')
        self.assertEqual('36.9181579_56.1266055', link_list[1], 'Coordinate 2 isn\'t correct')
        self.assertEqual('36.9229644_56.1225752', link_list[2], 'Coordinate 3 isn\'t correct')
        self.assertEqual('36.9085449_56.1304439', link_list[30], 'Coordinate 31 isn\'t correct')
        self.assertEqual('36.9126647_56.130252', link_list[31], 'Coordinate 32 isn\'t correct')

    def test_reading_coordinates(self):
        link_helper = LinkHelper()
        coord_list = link_helper.get_coordinates(test_link2)
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
        bbox_raw = link_helper.get_raw_bbox(test_link1)
        self.assertEqual('56.0997233901%2C36.7516463512%2C56.1797535595%2C37.0729964488',
                         bbox_raw, 'Bbox 1 isn\'t correct')
        bbox_raw = link_helper.get_raw_bbox(test_link2)
        self.assertEqual('', bbox_raw, 'Bbox 2 isn\'t correct')

    def test_reading_bbox(self):
        link_helper = LinkHelper()
        bbox_coord_list = link_helper.get_bbox(test_link1)

        self.assertEqual(2, len(bbox_coord_list), 'Bbox 1 list length isn\'t correct')
        self.assertEqual('36.7516463512', bbox_coord_list[0].longitude, 'Bbox coordinate 1 longitude isn\'t correct')
        self.assertEqual('56.0997233901', bbox_coord_list[0].latitude, 'Bbox coordinate 1 latitude isn\'t correct')
        self.assertEqual('37.0729964488', bbox_coord_list[1].longitude, 'Bbox coordinate 2 longitude isn\'t correct')
        self.assertEqual('56.1797535595', bbox_coord_list[1].latitude, 'Bbox coordinate 2 latitude isn\'t correct')

        bbox_coord_list = link_helper.get_bbox(test_link2)
        self.assertEqual(0, len(bbox_coord_list), 'Bbox 2 list length isn\'t correct')

    def test_reading_center(self):
        link_helper = LinkHelper()
        center = link_helper.get_center(test_link1)
        self.assertIsNone(center, 'Center isn\'t None')

        center = link_helper.get_center(test_link2)
        self.assertIsNotNone(center, 'Center is None')
        self.assertEqual('36.995401242747896', center.longitude, 'Center 2 longitude isn\'t correct')
        self.assertEqual('55.806737048576515', center.latitude, 'Center 2 latitude isn\'t correct')

    def test_reading_maxsite(self):
        link_helper = LinkHelper()
        maxsite = link_helper.get_maxsite(test_link1)
        self.assertEqual('250', maxsite, 'Maxsite 1 isn\'t correct')
        maxsite = link_helper.get_maxsite(test_link2)
        self.assertEqual('252', maxsite, 'Maxsite 2 isn\'t correct')

    def test_changing_coordinates(self):
        lh = LinkHelper()
        coordinate = Coordinate(longitude='36.9126647', latitude='56.130252')
        new_coordinate = lh.get_new_coordinate(coordinate)
        self.assertIsNotNone(new_coordinate)
        self.assertEqual(len(coordinate.longitude), len(new_coordinate.longitude), 'Longitude 1 length is not the same')
        self.assertEqual(len(coordinate.latitude), len(new_coordinate.latitude), 'Latitude 1 length is not the same')
        self.assertNotEqual(coordinate.longitude, new_coordinate.longitude, 'Longitude should not be the same')
        self.assertNotEqual(coordinate.latitude, new_coordinate.latitude, 'Latitude should not be the same')

        coordinate = Coordinate(longitude='36.995401242747896', latitude='55.806737048576515')
        new_coordinate = lh.get_new_coordinate(coordinate)
        self.assertIsNotNone(new_coordinate)
        self.assertEqual(len(coordinate.longitude), len(new_coordinate.longitude), 'Longitude 2 length is not the same')
        self.assertEqual(len(coordinate.latitude), len(new_coordinate.latitude), 'Latitude 2 length is not the same')
        self.assertNotEqual(coordinate.longitude, new_coordinate.longitude, 'Longitude should not be the same')
        self.assertNotEqual(coordinate.latitude, new_coordinate.latitude, 'Latitude should not be the same')

    def test_first_4_coordinate_digits_still_the_same(self):
        lh = LinkHelper()
        coordinate = Coordinate(longitude='36.9126647', latitude='56.130252')
        new_coordinate = lh.get_new_coordinate(coordinate)
        self.assertEqual(coordinate.latitude[:7], new_coordinate.latitude[:7])
        self.assertEqual(coordinate.longitude[:7], new_coordinate.longitude[:7])

        coordinate = Coordinate(longitude='36.995401242747896', latitude='55.806737048576515')
        new_coordinate = lh.get_new_coordinate(coordinate)
        self.assertEqual(coordinate.latitude[:7], new_coordinate.latitude[:7])
        self.assertEqual(coordinate.longitude[:7], new_coordinate.longitude[:7])

    def test_count_and_order_of_coordinates(self):
        pass

    def test_maxsite_modification(self):
        pass

    def test_bbox_modification(self):
        pass

    def test_center_modification(self):
        pass


if __name__ == '__main__':
    unittest.main()
