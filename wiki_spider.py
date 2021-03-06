from urllib.request import urlopen
from bs4 import BeautifulSoup
from dbdata import dbcountries, dbPageFields, dbPageFieldsSet
import csv
import time

# 匹配  different: {'马其顿', '波黑', '蒙古'}


def getCountry2href():
    html = urlopen(
        "https://zh.wikipedia.org/zh-cn/%E4%B8%96%E7%95%8C%E6%94%BF%E5%8D%80%E7%B4%A2%E5%BC%95")

    bs4Obj = BeautifulSoup(html, features="html.parser")
    tableList = bs4Obj.findAll("table", {"width": "90%"})

    # 所有国家的set
    country2href = {}
    for table in tableList:
        aTags = table.findAll("a")
        for tag in aTags:
            country = tag.get_text()
            rawRref = tag.attrs["href"]
            href = "https://zh.wikipedia.org/zh-cn/" + rawRref.split("/")[-1]
            country2href[country] = href

    return country2href


def getCountry2EngName():
    html = urlopen(
        "https://zh.wikipedia.org/zh-cn/%E4%B8%96%E7%95%8C%E6%94%BF%E5%8D%80%E7%B4%A2%E5%BC%95")

    bs4Obj = BeautifulSoup(html, features="html.parser")
    tableList = bs4Obj.findAll("table", {"width": "90%"})

    # 所有国家的set
    Country2EngName = {}
    for table in tableList:
        trs = table.tbody.findAll("tr")
        for tr in trs:
            country = tr.find("a").get_text()
            engName = ""
            if(len(tr.findAll("td")) >= 3):
                engName = tr.findAll("td")[2].get_text()

            Country2EngName[country] = engName

    return Country2EngName
# 对于一个国家, 生成一个map, 键值为在页面上找到的属性(未找到则没有键和值)


def Country2EngNamePrinter():
    Country2EngName = getCountry2EngName()
    for country in dbcountries:
        print(Country2EngName.get(country, country))


def pageExtractor(url):
    html = urlopen(url)
    bs4Obj = BeautifulSoup(html, features="html.parser")
    table = bs4Obj.find("table", {"class": "infobox"})

    resMap = {}
    if(table == None):
        return resMap

    for row in table.tbody.findAll("tr"):
        if row.th != None:  # 区分有无th的结构
            rowTitle = row.th.get_text()
            if dbPageFieldsSet.issuperset({rowTitle}):
                if row.td != None and row.th.get_text() == "GDP（国际汇率）":
                    resMap[rowTitle] = row.next_sibling.td.get_text()
                elif row.td != None:
                    resMap[rowTitle] = row.td.get_text()
                elif row.next_sibling.td != None:
                    resMap[rowTitle] = row.next_sibling.td.get_text()

        else:
            if(row.td.find("b") == None):
                continue
            rowTitle = row.td.find("b").get_text()
            if dbPageFieldsSet.issuperset({rowTitle}):
                resMap[rowTitle] = row.td.ul.get_text()

    return resMap


def mapPrinter(mapData):
    tmp = list(mapData)
    for i in tmp:
        print(i)
        print(mapData[i])


# 其中datamap刚好承接pageExtractor()的结果
def data2csv(writer, country, dataMap):
    print(dataMap)
    countryDataList = [country]
    for field in dbPageFields:
        fieldData = dataMap.get(field, None)
        if fieldData != None:
            countryDataList.append(fieldData)
        else:
            countryDataList.append("")
    writer.writerow(countryDataList)


def main():
    # saving options
    file = open('wiki_world.csv', 'w', newline='', encoding='utf8')
    file.write('\ufeff')
    writer = csv.writer(file)
    writer.writerow(["国家"] + dbPageFields)

    # loop countries
    Country2href = getCountry2href()
    count = 0
    for country in dbcountries:
        countryMap = pageExtractor(
            Country2href[country])
        data2csv(writer, country, countryMap)

        print(count, " ", country, " ", len(countryMap))
        count += 1
    # file closed
    file.close()


def mainFiltered(start, end):
    # saving options
    file = open('wiki_world.csv', 'w', newline='', encoding='utf8')
    file.write('\ufeff')
    writer = csv.writer(file)
    writer.writerow(["国家"] + dbPageFields)

    # loop countries
    Country2href = getCountry2href()
    count = 0
    for i in range(start, end):
        country = dbcountries[i]
        countryMap = pageExtractor(
            Country2href[country])
        data2csv(writer, country, countryMap)

        print(count, " ", country, " ", len(countryMap))
        count += 1
    # file closed
    file.close()

# main()


Country2EngNamePrinter()
