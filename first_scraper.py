from urllib.request import urlopen

from loaders.simple_reader import SimpleReader

url = "http://olympus.realpython.org/profiles/aphrodite"
html = SimpleReader().read_url(url)

print(html)
