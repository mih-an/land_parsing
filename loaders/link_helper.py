import random


class Coordinate:

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class LinkHelper:
    coord_start_str = 'in_polygon%5B1%5D='
    coord_start_addition_str = ''
    coord_separator = '%2C'
    lon_lat_separator = '_'
    bbox_start_str = 'bbox='
    center_start_str = 'center='
    maxsite_start_str = 'maxsite='
    url_param_separator = '&'
    coord_modification_start_pos = 7
    coord_modification_end_pos = 10
    len_gen_number = 3
    max_site_start = 230
    max_site_end = 270
    max_site_default = 250

    def find_substr(self, url, substr_start):
        substr_pos_start = url.find(substr_start)
        if substr_pos_start == -1:
            return ''

        substr_pos_start = substr_pos_start + len(substr_start)
        result_substr = url[substr_pos_start:]
        substr_pos_end = result_substr.find(self.url_param_separator)
        result_substr = result_substr[:substr_pos_end]
        return result_substr

    def find_coord_substr(self, url: str):
        return self.find_substr(url, self.coord_start_str)

    def find_bbox_substr(self, url: str):
        return self.find_substr(url, self.bbox_start_str)

    def read_raw_coordinates(self, url: str):
        coord_substr = self.find_coord_substr(url)
        if coord_substr == '':
            return []
        return coord_substr.split(self.coord_separator)

    def read_coordinates(self, url: str):
        coord_raw_list = self.read_raw_coordinates(url)
        coord_list = []
        for coord_raw in coord_raw_list:
            tmp_list = coord_raw.split(self.lon_lat_separator)
            coord = Coordinate(longitude=tmp_list[0], latitude=tmp_list[1])
            coord_list.append(coord)

        return coord_list

    def read_raw_bbox(self, url: str):
        return self.read_raw_substr_from_link(url, self.bbox_start_str)

    def read_raw_center(self, url: str):
        return self.read_raw_substr_from_link(url, self.center_start_str)

    def read_raw_substr_from_link(self, url: str, substr: str):
        substr_start_pos = url.find(substr)
        if substr_start_pos == -1:
            return ''
        substr_start_pos = substr_start_pos + len(substr)
        substr = url[substr_start_pos:]
        substr_end_pos = substr.find(self.url_param_separator)
        return substr[:substr_end_pos]

    def read_bbox(self, url: str):
        raw_bbox = self.read_raw_bbox(url)
        if raw_bbox == '':
            return []

        latlon_list = raw_bbox.split(self.coord_separator)
        # There are always 2 coordinates in bbox parameter
        coord1 = Coordinate(longitude=latlon_list[1], latitude=latlon_list[0])
        coord2 = Coordinate(longitude=latlon_list[3], latitude=latlon_list[2])

        return [coord1, coord2]

    def read_center(self, url: str):
        raw_center = self.read_raw_center(url)
        if raw_center == '':
            return None

        point_list = raw_center.split(self.coord_separator)
        # There is always only one coordinate
        coordinate = Coordinate(longitude=point_list[1], latitude=point_list[0])

        return coordinate

    def read_maxsite(self, url: str):
        maxsite_str = self.read_raw_substr_from_link(url, self.maxsite_start_str)
        return maxsite_str

    def gen_one_new_coord(self, base_coord: str):
        # Too short coordinate to modify
        if len(base_coord) < self.coord_modification_start_pos:
            return base_coord

        new_coord_part = str(random.randint(100, 999))
        new_coord = base_coord[:self.coord_modification_start_pos] + new_coord_part

        # Shortage to base_coordinate length
        if len(new_coord) > len(base_coord):
            new_coord = new_coord[:len(base_coord)]
        # Restore a tail of long base coordinate
        if len(base_coord) > len(new_coord):
            new_coord = new_coord + base_coord[self.coord_modification_start_pos + self.len_gen_number:]

        return new_coord

    def gen_new_coordinate(self, base_coordinate: Coordinate):
        """
        Generates new coordinate with different digits but the same meaning
        Because all coordinates have different length function will change only [4:7] digits after '.' separator
        If length is not enough it generate additional digits but cut it to the previous length
        If length is more than needed it generate only 3 unique digits and add tail without modification
        If length is less than coord_modification_start_pos there is no modification
        :param base_coordinate: base coordinate
        :return: New coordinate with new digits after 4 digits after dot
        """

        new_longitude = self.gen_one_new_coord(base_coordinate.longitude)
        new_latitude = self.gen_one_new_coord(base_coordinate.latitude)
        new_coordinate = Coordinate(longitude=new_longitude, latitude=new_latitude)

        return new_coordinate

    def gen_new_coordinates(self, url: str):
        coord_list = self.read_coordinates(url)
        new_coord_list = []
        for i in range(len(coord_list)):
            coord = coord_list[i]
            if i < len(coord_list) - 1:
                new_coord = self.gen_new_coordinate(coord)
            else:
                # First and last coordinates should be the same
                new_coord = Coordinate(new_coord_list[0].longitude, new_coord_list[0].latitude)
            new_coord_list.append(new_coord)

        return new_coord_list

    def gen_new_maxsite_int(self):
        new_maxsite = random.randint(self.max_site_start, self.max_site_end)
        # For testing purpose
        if new_maxsite == self.max_site_default:
            new_maxsite += 1
        return new_maxsite

    def gen_new_link_with_new_coordinates(self, url: str):
        coord_substr = self.find_coord_substr(url)
        if coord_substr == '':
            return url

        new_coordinates = self.gen_new_coordinates(url)
        new_url_coord_str = self.coordinates_to_url_str(new_coordinates)

        return url.replace(coord_substr, new_url_coord_str)

    def gen_new_link_with_new_center(self, url):
        center_substr = self.find_substr(url, self.center_start_str)
        if center_substr == '':
            return url

        center = self.read_center(url)
        if center is None:
            return url

        coord = self.gen_new_coordinate(center)
        new_url = self.center_to_url_str(coord)

        return url.replace(center_substr, new_url)

    def gen_new_link_with_new_maxsite(self, url):
        maxsite_substr = self.find_substr(url, self.maxsite_start_str)
        if maxsite_substr == '':
            return url

        new_maxsite_int = self.gen_new_maxsite_int()

        return url.replace(maxsite_substr, f'{new_maxsite_int}')

    def gen_new_link_with_new_bbox(self, url):
        bbox_substr = self.find_bbox_substr(url)
        if bbox_substr == '':
            return url

        bbox = self.read_bbox(url)
        if len(bbox) == 0:
            return url

        coord1 = Coordinate(longitude=bbox[0].longitude, latitude=bbox[0].latitude)
        coord2 = Coordinate(longitude=bbox[1].longitude, latitude=bbox[1].latitude)

        coord1 = self.gen_new_coordinate(coord1)
        coord2 = self.gen_new_coordinate(coord2)
        new_url_bbox_str = self.bbox_to_url_str([coord1, coord2])

        return url.replace(bbox_substr, new_url_bbox_str)

    def gen_new_unique_url(self, url: str):
        """
        Replace all coordinates with the new ones - generated
        All coordinates move insignificantly but enough to be unique
        :param url: base url to modify
        :return: modified url
        """
        new_url = self.gen_new_link_with_new_coordinates(url)
        new_url = self.gen_new_link_with_new_bbox(new_url)
        new_url = self.gen_new_link_with_new_center(new_url)
        new_url = self.gen_new_link_with_new_maxsite(new_url)

        return new_url

    def coordinates_to_url_str(self, coord_list: [Coordinate]):
        return self.data_to_url_str(coord_list, self.lon_lat_separator, self.coord_separator)

    def bbox_to_url_str(self, coord_list: [Coordinate]):
        return self.data_to_url_str(coord_list, self.coord_separator, self.coord_separator, True)

    @staticmethod
    def data_to_url_str(coord_list, sep1, sep2, is_reverse=False):
        result_str = ''
        for i in range(len(coord_list)):
            coord = coord_list[i]
            coord_str = f'{coord.longitude}{sep1}{coord.latitude}'
            if is_reverse:
                coord_str = f'{coord.latitude}{sep1}{coord.longitude}'

            if i < len(coord_list) - 1:
                result_str += coord_str + sep2
            else:
                result_str += coord_str

        return result_str

    def center_to_url_str(self, center):
        return self.data_to_url_str([center], self.coord_separator, self.coord_separator, True)
