from urllib.request import urlopen

from loaders.simple_reader import SimpleReader

url = "http://olympus.realpython.org/profiles/aphrodite"
simple_reader = SimpleReader()
html = simple_reader.read_url(url)
title = simple_reader.get_title(html)

print(title)
