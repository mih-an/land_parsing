from loaders.land_parser import LandParser

url = ("https://cian.ru/cat.php?engine_version=2&p=1&region=1&offer_type=flat&deal_type=rent&room2=1"
       "&room3=1&with_neighbors=0&type=4")

lp = LandParser()
res = lp.load_page(url)

print(res.status_code)
with open("output.html", 'a') as f:
    f.write(res.text)
