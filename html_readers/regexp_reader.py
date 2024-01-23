from bs4 import BeautifulSoup


class HtmlReader:

    @staticmethod
    def get_links(html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        links_tag = soup.find_all("a")

        link_lst = []
        for link in links_tag:
            link_lst.append("http://olympus.realpython.org" + link["href"])

        return link_lst
