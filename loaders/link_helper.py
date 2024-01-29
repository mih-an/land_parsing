import random


class Coordinate:

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class LinkHelper:
    coord_start_str = 'in_polygon'
    coord_start_addition_str = '%5B1%5D='
    coord_separator = '%2C'
    split_longitude_latitude = '_'
    bbox_start_str = 'bbox='
    center_start_str = 'center='
    maxsite_start_str = 'maxsite='
    url_param_separator = '&'
    coord_modification_start_pos = 7
    coord_modification_end_pos = 10
    len_gen_number = 3

    def get_raw_coordinates(self, url: str):
        coord_pos_start = url.find(self.coord_start_str)
        if coord_pos_start == -1:
            return []

        coord_pos_start = coord_pos_start + len(self.coord_start_str) + len(self.coord_start_addition_str)
        coord_substr = url[coord_pos_start:]
        coord_pos_end = coord_substr.find(self.url_param_separator)
        coord_substr = coord_substr[:coord_pos_end]
        coord_list = coord_substr.split(self.coord_separator)

        return coord_list

    def get_coordinates(self, url: str):
        coord_raw_list = self.get_raw_coordinates(url)
        coord_list = []
        for coord_raw in coord_raw_list:

            tmp_list = coord_raw.split(self.split_longitude_latitude)
            coord = Coordinate(longitude=tmp_list[0], latitude=tmp_list[1])
            coord_list.append(coord)

        return coord_list

    def get_raw_bbox(self, url: str):
        return self.get_raw_substr_from_link(url, self.bbox_start_str)

    def get_raw_center(self, url: str):
        return self.get_raw_substr_from_link(url, self.center_start_str)

    def get_raw_substr_from_link(self, url: str, substr: str):
        substr_start_pos = url.find(substr)
        if substr_start_pos == -1:
            return ''
        substr_start_pos = substr_start_pos + len(substr)
        substr = url[substr_start_pos:]
        substr_end_pos = substr.find(self.url_param_separator)
        return substr[:substr_end_pos]

    def get_bbox(self, url: str):
        raw_bbox = self.get_raw_bbox(url)
        if raw_bbox == '':
            return []

        latlon_list = raw_bbox.split(self.coord_separator)
        # There are always 2 coordinates in bbox parameter
        coord1 = Coordinate(longitude=latlon_list[1], latitude=latlon_list[0])
        coord2 = Coordinate(longitude=latlon_list[3], latitude=latlon_list[2])

        return [coord1, coord2]

    def get_center(self, url: str):
        raw_center = self.get_raw_center(url)
        if raw_center == '':
            return None

        point_list = raw_center.split(self.coord_separator)
        # There is always only one coordinate
        coordinate = Coordinate(longitude=point_list[1], latitude=point_list[0])

        return coordinate

    def get_maxsite(self, url: str):
        maxsite_str = self.get_raw_substr_from_link(url, self.maxsite_start_str)
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

    def get_new_coordinate(self, base_coordinate: Coordinate):
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
