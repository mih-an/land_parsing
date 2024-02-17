import re


class ParseHelper:
    def __init__(self):
        # https://regex101.com/r/Kb2L0r/2
        self.kadastr_pattern = '\d{2}:\d{2}:\d{6,7}:\d*'
        self.float_pattern = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
        self.title_separator = ', '
        self.square_sot = 'сот.'
        self.square_m2 = 'м²'
        self.square_ga = 'га'
        self.int_pattern = '\D'

    def parse_kadastr(self, description: str):
        kadastr_list = []

        search_res = re.search(self.kadastr_pattern, description)
        if search_res is not None:
            for catch in re.finditer(self.kadastr_pattern, description):
                kadastr_list.append(catch[0])

        return kadastr_list

    def search_float_number(self, search_str):
        if re.search(self.float_pattern, search_str) is not None:
            for catch in re.finditer(self.float_pattern, search_str):
                result_float_number = float(catch[0])
                return result_float_number
        return 0

    def parse_square(self, search_str):
        title_segment_list = search_str.split(self.title_separator)

        is_sot_found = False
        for segment in title_segment_list:
            if self.square_sot in segment:
                needed_segment = segment
                return self.search_float_number(needed_segment)

        if not is_sot_found and self.square_m2 in search_str:
            square_m2 = self.search_float_number(search_str)
            return square_m2 / 100

        if not is_sot_found and self.square_ga in search_str:
            square_ga = self.search_float_number(search_str)
            return square_ga * 100

        return 0

    def search_int_number(self, search_str):
        search_res = re.sub(self.int_pattern, "", search_str)
        if search_res == '':
            return 0
        return int(search_res)
