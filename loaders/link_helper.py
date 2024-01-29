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
