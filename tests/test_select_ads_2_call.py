import unittest
import uuid

from calling_bp.calling_bp import CallBusinessProcess
from db.ads_database import AdsDataBase
from tests.test_helper import TestHelper


# Как я хочу, чтобы это работало.
# Я хочу, чтобы не менее 50 объявлений каждый день попадало на прозвон на актуализацию информации
# Если по ним не дозвонились, что эти объявления должны быть прозвонены второй раз и третий раз
# Если по ним на звонке не удалось собрать информацию, то эту информацию нужно дособрать на следующий день
# или через день, то есть тогда, когда эта информация появится у владельца или агента.
# Каждый день появляются новые объявления по секторам. Причем по тем, по которым уже звонили ранее.
# Как их приоритезировать? Должны ли они идти раньше объявления из новых секторов или нет? Непонятно.
# Скорее нет, чем да. Важнее иметь информацию по секторам, по которым уже сделана работа, нежели по совершенно новым.
# Ладно, допустим я вручную задам приоритет секторов по их интересности мне самому.
# И обработка будет вестись в соотвествии с этим приоритетом. Да, наверное, это самый лучший способ
#
# Новые объявления из сектора попадают на прозвон в количестве не менее 50 штук в день.
# Видимо, надо сохранять отправленные на прозвон либо в отдельной таблице, либо завести статус в основной таблице
# Нужно ли ограничивать отправку на прозвон по 50 штук в день или сразу бухнуть в амоцрм всю пачку?
# Наверное, особого смысла бахать всю пачку нет, т.к. их всё равно никто не прозвонит, и они могут быть сняты с
# публикации до момента звонка. Поэтому приходим к выводу, что надо ограничивать по 50 штук в день всё таки.
#
# Какие тесты надо написать
# 1. Статус - нужно понимать, было ли данное объявление отправлено на прозвон и когда?
# 2. (done) Отправить на прозвон одно объявление + проверить статус
# 3. (done) Отправить на прозвон группу объявлений + проверить статус, что было отправлено
# 4. Выбор на прозвон 50 штук объявлений новых
# 5. Выбор на прозвон только тех, кто не снят с публикации
# 6. Выбор на прозвон только тех, кто до этого еще не был отправлен на прозвон
# 7. Выбор на прозвон только 50 штук, но с учетом снятых и уже отправленных
# 8. Не отправлять на проверку "снят с публикации" те объявления, которые только сегодня были созданы/актуализированы
# 9. Отправить конкретному менеджеру на прозвон
# 10. Не отправлять на прозвон электронные торги


class TestCaseSelectAds2Call(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    def test_set_ads_to_call(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.test_helper.create_test_ads2(ads2_uuid)
        ads_list = [ads1, ads2]
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.save_to_call(ads_list)

        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(2, len(ads_list_to_call))
        self.test_helper.check_ads_are_equal(ads1, ads_list_to_call[0])
        self.test_helper.check_ads_are_equal(ads2, ads_list_to_call[1])

    def test_50_ads_to_call(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list1 = []
        for i in range(50):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads_list1.append(ads)

        ads_list2 = []
        for i in range(50):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads2(ads_uuid)
            ads.sector_number = 5110
            ads_list2.append(ads)

        ads_list = []
        ads_list.extend(ads_list1)
        ads_list.extend(ads_list2)
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.select_portion_to_call()
        ads_list_to_call = cbp.load_ads_list_to_call()

        self.assertEqual(50, len(ads_list_to_call))
        for ads in ads_list_to_call:
            self.assertEqual(ads.sector_number, 4110)

        cbp.select_portion_to_call()
        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(100, len(ads_list_to_call))
        ads_list_to_call = ads_list_to_call[50:]
        for ads in ads_list_to_call:
            self.assertEqual(ads.sector_number, 5110)


if __name__ == '__main__':
    unittest.main()
