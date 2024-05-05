import unittest

from tests.test_helper import TestHelper


# Как я хочу, чтобы это работало.
#
class TestCaseSelectAds2Call(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_select_ads_to_call(self):
        # Cоздаем несколько тестовых объявлений в тестовом секторе (-1 сектор) На проверку снятости должны попадать
        # только те объявления, которые
        # а) Не имеют явного флага "снято с публикации"
        # б) Те, дата обновления которых не равна сегодняшней дате, так как очевидно, что они были обновлены только
        # сегодня, а значит с продажи были не сняты
        # в) Те, которые еще не были отправлены на прозвон в амоцрм

        # ads1_uuid = str(uuid.uuid4())
        # ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        # ads2_uuid = str(uuid.uuid4())
        # ads2 = self.test_helper.create_test_ads2(ads2_uuid)
        # ads_list = [ads1, ads2]
        # ads_db = AdsDataBase()
        # ads_db.save(ads_list)
        pass

        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
