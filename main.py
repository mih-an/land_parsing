import sys
from datetime import datetime

from calling_bp.calling_bp import CallBusinessProcess
from parsing_worker import ParsingWorker

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "insert_ads_to_call":
        cbp = CallBusinessProcess()
        count_to_add = 50
        if len(sys.argv) == 3:
            count_to_add = sys.argv[2]
        cbp.insert_ads_to_call(count_to_add, datetime.now())
        exit()

    parsing_worker = ParsingWorker()
    parsing_worker.parse_and_save_ads_from_cian()
    parsing_worker.copy_new_ads_to_google_sheet()
