import unittest
import uuid

from calling_bp.calling_bp import CallBusinessProcess
from db.ads_database import AdsDataBase
from tests.test_helper import TestHelper
from datetime import timedelta, datetime


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
# 1. (done) Статус - нужно понимать, было ли данное объявление отправлено на прозвон
# 2. (done) Отправить на прозвон одно объявление + проверить статус
# 3. (done) Отправить на прозвон группу объявлений + проверить статус, что было отправлено
# 4. (done) Выбор на прозвон 50 штук объявлений новых
# 5. (done) Выбор на прозвон только тех, кто не снят с публикации
# 6. (done) Выбор на прозвон только тех, кто до этого еще не был отправлен на прозвон
# 7. (done) Проверка снятия с публикации перед отправкой на прозвон
# 8. (done) Не отправлять на проверку снятия с публикации те объявления, которые только сегодня были актуализированы
# 10. (done) Не отправлять на прозвон электронные торги
# 11. Сохранять и загружать дату отправки на прозвон
# 13. Выгружать в гугл таблицу на прозвон
# 14. Приоритет по секторам на проде сделать
# 15. Исправить баг, когда можно добавить на прозвон снятое с публикации объявление
# 16. Сделать параметр по количеству добавляемых на прозвон объявлений

# Позже:
# Отправить конкретному менеджеру на прозвон
# Не отправлять больше 50 штук на прозвон в одну дату - не уверен, что это надо


class TestCaseSelectAds2Call(unittest.TestCase):
    def setUp(self):
        self.test_helper = TestHelper()

    # Отправить на прозвон одно объявление + проверить статус
    # Отправить на прозвон группу объявлений + проверить статус, что было отправлено
    def test_set_ads_to_call(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads1.electronic_trading = ''
        ads1.is_electronic_trading = False
        ads1.link = 'dont_check'
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.test_helper.create_test_ads2(ads2_uuid)
        ads2.link = 'dont_check'
        ads2.electronic_trading = ''
        ads2.is_electronic_trading = False
        ads_list = [ads1, ads2]
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        # cbp.insert_ads_to_call(50, datetime.now())
        cbp.save_to_call(ads_list)

        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(2, len(ads_list_to_call))
        self.test_helper.check_ads_are_equal(ads1, ads_list_to_call[0])
        self.test_helper.check_ads_are_equal(ads2, ads_list_to_call[1])

    # Выбор на прозвон 50 штук объявлений новых
    def test_50_ads_to_call(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list1 = []
        for i in range(50):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads.link = 'dont_check'
            ads.electronic_trading = ''
            ads.is_electronic_trading = False
            ads_list1.append(ads)

        ads_list2 = []
        for i in range(50):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads2(ads_uuid)
            ads.sector_number = 5110
            ads.link = 'dont_check'
            ads_list2.append(ads)

        ads_list = []
        ads_list.extend(ads_list1)
        ads_list.extend(ads_list2)
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(50, datetime.now())
        ads_list_to_call = cbp.load_ads_list_to_call()

        self.assertEqual(50, len(ads_list_to_call))
        for ads in ads_list_to_call:
            self.assertEqual(ads.sector_number, 4110)

        # cbp.insert_portion_to_call()
        cbp.insert_ads_to_call(50, datetime.now())
        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(100, len(ads_list_to_call))
        ads_list_to_call = ads_list_to_call[50:]
        for ads in ads_list_to_call:
            self.assertEqual(ads.sector_number, 5110)

    # Выбор на прозвон только тех, кто до этого еще не был отправлен на прозвон
    def test_to_call_only_once(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list = []
        for i in range(50):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads.link = 'dont_check'
            ads.electronic_trading = ''
            ads.is_electronic_trading = False
            ads_list.append(ads)
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(50, datetime.now())
        cbp.insert_ads_to_call(50, datetime.now())
        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(50, len(ads_list_to_call))
        for ads in ads_list_to_call:
            self.assertEqual(ads.sector_number, 4110)

    # Выбор на прозвон только тех, кто не снят с публикации
    def test_to_call_only_published(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list = []
        for i in range(50):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads.link = 'dont_check'
            ads.electronic_trading = ''
            ads.is_electronic_trading = False
            ads_list.append(ads)
        ads_list[0].is_unpublished = True
        ads_list[10].is_unpublished = True
        ads_list[49].is_unpublished = True
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(50, datetime.now())
        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(47, len(ads_list_to_call))

    # Проверка снятия с публикации перед отправкой на прозвон
    def test_unpublished_before_to_call(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list = []
        for i in range(50):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads.link = 'dont_check'
            ads.electronic_trading = ''
            ads.is_electronic_trading = False
            ads_list.append(ads)
        # Real unpublished ads
        ads_list[0].link = 'https://www.cian.ru/sale/suburban/291001135/'
        # need to age ads because we don't check fresh ads
        ads_list[0].last_parse_datetime = ads_list[0].last_parse_datetime - timedelta(days=2)
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(50, datetime.now())
        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(49, len(ads_list_to_call))
        for ads in ads_list_to_call:
            self.assertNotEqual(ads.link, 'https://www.cian.ru/sale/suburban/291001135/')

    # Не отправлять на проверку "снят с публикации" те объявления, которые только сегодня были созданы/актуализированы
    # Так как они с большое вероятностью еще не сняты, а лишний раз ходить в сеть за проверкой ни к чему
    def test_dont_check_new_ads(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list = []
        for i in range(10):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            # Real unpublished ads
            ads.link = 'dont_check'
            ads.electronic_trading = ''
            ads.is_electronic_trading = False
            ads_list.append(ads)

        # Only one ads should be checked for unpublished status
        ads_list[0].link = 'https://www.cian.ru/sale/suburban/291001135/'
        ads_list[0].last_parse_datetime = ads_list[0].last_parse_datetime - timedelta(days=2)
        # despite ads link is really unpublished they shouldn't be checked because they are fresh
        ads_list[1].link = 'https://www.cian.ru/sale/suburban/291001135/'
        ads_list[2].link = 'https://www.cian.ru/sale/suburban/291001135/'
        ads_list[9].link = 'https://www.cian.ru/sale/suburban/291001135/'
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(50, datetime.now())
        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(9, len(ads_list_to_call))

    # Нет смысла отправлять на прозвон электронные торги
    def test_dont_send_to_call_electronic_trades(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list = []
        for i in range(50):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads.link = 'dont_check'
            ads_list.append(ads)

        ads_list[0].electronic_trading = ''
        ads_list[0].is_electronic_trading = False
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(50, datetime.now())
        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(1, len(ads_list_to_call))

    # Проверка статуса объявления - отправлено ли на прозвон
    def test_check_ads_is_inserted_to_call(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        # Create and save new ads
        ads1_uuid = str(uuid.uuid4())
        ads1 = self.test_helper.create_test_ads1(ads1_uuid)
        ads1.sector_number = 4110
        ads1.link = 'dont_check'
        ads1.electronic_trading = ''
        ads1.is_electronic_trading = False
        ads_list = [ads1]
        ads_db.save(ads_list)
        # move it to call
        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(50, datetime.now())

        # create and save new ads, but don't move it to call
        ads2_uuid = str(uuid.uuid4())
        ads2 = self.test_helper.create_test_ads2(ads2_uuid)
        ads2.sector_number = 4110
        ads2.link = 'dont_check'
        ads_list = [ads2]
        ads_db.save(ads_list)

        # first ads should be sent to call and the second shouldn't
        ads_to_call1 = cbp.check_ads_to_call(ads1_uuid)
        self.test_helper.check_ads_are_equal(ads1, ads_to_call1)
        ads_to_call2 = cbp.check_ads_to_call(ads2_uuid)
        self.assertIsNone(ads_to_call2)

    # Отправляем на прозвон на произвольную дату и проверяем загрузку этой даты
    # Это нужно, чтобы в будущем понимать, какие объявления и когда были отправлены на прозвон
    def test_save_mix_date_to_call(self):
        pass
        # ads_db = AdsDataBase()
        # cbp = CallBusinessProcess()
        # ads_db.delete_test_ads()
        # two_days_ago = datetime.now() - timedelta(days=2)
        #
        # ads_list = []
        # for i in range(10):
        #     ads_uuid = str(uuid.uuid4())
        #     ads = self.test_helper.create_test_ads1(ads_uuid)
        #     ads.sector_number = 4110
        #     ads.link = 'dont_check'
        #     ads.electronic_trading = ''
        #     ads.is_electronic_trading = False
        #     ads_list.append(ads)
        # ads_db.save(ads_list)
        # ads_id_from_today = ads_list[0].id
        # cbp.insert_portion_to_call()
        #
        # ads_list = []
        # for i in range(7):
        #     ads_uuid = str(uuid.uuid4())
        #     ads = self.test_helper.create_test_ads1(ads_uuid)
        #     ads.sector_number = 4110
        #     ads.link = 'dont_check'
        #     ads.electronic_trading = ''
        #     ads.is_electronic_trading = False
        #     ads_list.append(ads)
        # ads_db.save(ads_list)
        # ads_id_from_two_days_ago = ads_list[0].id
        # cbp.insert_portion_to_call_with_date(two_days_ago)
        #
        # ads_list_to_call = cbp.load_ads_list_to_call_by_date(two_days_ago)
        # self.assertEqual(7, len(ads_list_to_call))
        # ads_list_to_call = cbp.load_ads_list_to_call_by_date(datetime.now())
        # self.assertEqual(10, len(ads_list_to_call))
        #
        # # check if ads has correct date to call
        # ads_from_today = cbp.check_ads_to_call(ads_id_from_today)
        # ads_from_two_days_ago = cbp.check_ads_to_call(ads_id_from_two_days_ago)
        #
        # delta1 = datetime.now() - ads_from_today.date_to_call
        # delta2 = datetime.now() - ads_from_two_days_ago.date_to_call
        # self.assertEqual(delta1.days, 0)
        # self.assertEqual(delta2.days, 2)

    # may be bug можно отправить на прозвон неопубликованные
    # для этого нужно создать 51 объявление. Последние 2 снятые с публикации. И отправить на прозвоню
    # добавится 50 вместо 49.
    def test_maybe_bug(self):
        # pass
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list = []
        for i in range(51):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads.link = 'dont_check'
            ads.electronic_trading = ''
            ads.is_electronic_trading = False
            ads_list.append(ads)

        ads_list[49].link = 'https://www.cian.ru/sale/suburban/291001135/'
        ads_list[49].last_parse_datetime = ads_list[0].last_parse_datetime - timedelta(days=2)
        ads_list[50].link = 'https://www.cian.ru/sale/suburban/291001135/'
        ads_list[50].last_parse_datetime = ads_list[0].last_parse_datetime - timedelta(days=2)
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(50, datetime.now())
        ads_list_to_call = cbp.load_ads_list_to_call()
        self.assertEqual(49, len(ads_list_to_call))

    def test_ads_to_call_with_count_param(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list = []
        for i in range(10):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads.link = 'dont_check'
            ads.electronic_trading = ''
            ads.is_electronic_trading = False
            ads_list.append(ads)
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(5, datetime.now())
        ads_to_call_list = cbp.load_ads_list_to_call()
        self.assertEqual(5, len(ads_to_call_list))

    def test_ads_to_call_more_than_exist(self):
        ads_db = AdsDataBase()
        ads_db.delete_test_ads()

        ads_list = []
        for i in range(5):
            ads_uuid = str(uuid.uuid4())
            ads = self.test_helper.create_test_ads1(ads_uuid)
            ads.sector_number = 4110
            ads.link = 'dont_check'
            ads.electronic_trading = ''
            ads.is_electronic_trading = False
            ads_list.append(ads)
        ads_db.save(ads_list)

        cbp = CallBusinessProcess()
        cbp.insert_ads_to_call(10, datetime.now())
        ads_to_call_list = cbp.load_ads_list_to_call()
        self.assertEqual(5, len(ads_to_call_list))

    def test_unpublished_more_than_needed_to_call(self):
        pass


if __name__ == '__main__':
    unittest.main()
