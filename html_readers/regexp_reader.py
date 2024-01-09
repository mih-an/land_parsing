import re


class HtmlReader:
    @staticmethod
    def get_title(test_html):
        pattern = "<title.*?>.*?</title.*?>"
        match_results = re.search(pattern, test_html, re.IGNORECASE)
        title = match_results.group()
        # Remove HTML tags
        title = re.sub("<.*?>", "", title)
        return title

    @staticmethod
    def get_name(test_html):
        pattern = "Name:.*?<"
        match_results = re.search(pattern, test_html, re.IGNORECASE)
        name = match_results.group()
        # Remove HTML tags and Name:
        name = re.sub("<.*?", "", name)
        name = re.sub("Name: ", "", name)
        return name

    @staticmethod
    def get_fav_color(test_html):
        pattern = "Favorite Color:.*"
        match_results = re.search(pattern, test_html, re.IGNORECASE)
        fav_wine = match_results.group()
        fav_wine = re.sub("Favorite Color: ", "", fav_wine)
        return fav_wine
