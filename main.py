import mechanicalsoup

# 1
browser = mechanicalsoup.Browser()
url = "https://www.avito.ru/moskva_i_mo/zemelnye_uchastki/prodam/izhs-ASgBAQICAUSWA9oQAUCmCBTmVQ?p=2"
login_page = browser.get(url)
login_html = login_page.soup
print(login_html)

# # 2
# form = login_html.select("form")[0]
# form.select("input")[0]["value"] = "zeus"
# form.select("input")[1]["value"] = "ThunderDude"
#
# # 3
# profiles_page = browser.submit(form, login_page.url)
# print(profiles_page.soup.title)
