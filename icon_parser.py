import requests as req
from lxml import etree

def get_icon_by_word(word, filepath="output.png"):
    ans = req.get("https://icon-icons.com/ru/Поиск/иконки/?filtro={}&style=1".format(word))

    html = etree.HTML(ans.text)
    xpath = etree.XPath('//div[@id="0"]//button')
    if len(xpath(html)) == 0:
        return None

    download_url = r"https://icon-icons.com/" + xpath(html)[0].get("onclick").split("'")[1]

    icon_page = req.get(download_url)
    html = etree.HTML(icon_page.text)
    xpath = etree.XPath('//div[@class="container-fluid"]//h2//a')
    download_url = xpath(html)[0].get("href")

    print(download_url)
    icon = req.get(download_url)
    print(icon)
    print(icon.content)
    f = open(filepath, 'wb')
    f.write(icon.content)
    f.close()

get_icon_by_word("бережочек")
