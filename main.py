from parsing_worker import ParsingWorker

if __name__ == "__main__":
    parsing_worker = ParsingWorker()
    parsing_worker.parse_and_save_ads_from_cian()
    parsing_worker.copy_new_ads_to_google_sheet()
