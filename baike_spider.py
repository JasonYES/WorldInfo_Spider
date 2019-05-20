from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
from dbdata import dbcountries, dbPageFields, dbPageFieldsSet, dbPageFields_Baike
import csv
from time import sleep

# baike spider


def getAIanswer(country, field):

    searchWord = urllib.parse.quote_plus(country + " " + field)
    url = "https://www.baidu.com/from=844b/s?word=" + searchWord + \
        "&ts=5486044&t_kt=0&ie=utf-8&fm_kl=021394be2f&rsv_iqid=3477954786&rsv_t=bbacTsfRkjUEfPXSLIkE13%252B3eIjmkbytLVToIZ15XxYWJoGsa3F%252BjWHePA&sa=ib&ms=1&rsv_pq=3477954786&rsv_sug4=5079&ss=100000000001&inputT=2598&tj=1"
    html = urlopen(url)

    bs4Obj = BeautifulSoup(html, features="html.parser")

    answer = bs4Obj.find(  # 尝试第一种格式
        "p", {"class": "c-line-clamp3 wa-ks-general-bottom-margin3 wa-ks-general-name c-gap-top-small c-color-link wa-ks-general-fontSize24"})
    if answer == None:  # 可能的另一种格式
        answer = bs4Obj.find(
            "p", {"class": "c-line-clamp3 wa-ks-general-bottom-margin3 wa-ks-general-name c-gap-top-small c-color-link wa-ks-general-fontSize19"})
    if answer == None:  # 可能的另一种格式
        answer = bs4Obj.find(
            "p", {"class": "wa-population-chart-prefix wa-population-chart-main c-title"})
    if answer == None:  # 可能的另一种格式
        answer = bs4Obj.find(
            "p", {"class": "c-line-clamp3 c-gap-top-small wa-ks-general-fontSize24"})
    if answer == None:  # 可能的另一种格式
        answer = bs4Obj.find(
            "p", {"class": "c-line-clamp3 c-gap-top-small wa-ks-general-fontSize19"})
    if answer == None:  # 就此放弃
        return ""

    return answer.get_text()


# 对于一个国家, 生成一个map, 键值为在页面上找到的属性

def countryExtractor(country):

    resMap = {}
    for f in dbPageFields_Baike:
        fieldData = getAIanswer(country, f)
        resMap[f] = fieldData

    # sleep(1)

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
    for field in dbPageFields_Baike:
        fieldData = dataMap.get(field, None)
        if fieldData != None:
            countryDataList.append(fieldData)
        else:
            countryDataList.append("")
    writer.writerow(countryDataList)


def mainFiltered(start, end):
    # saving options
    file = open('baike_world.csv', 'w', newline='', encoding='utf8')
    file.write('\ufeff')
    writer = csv.writer(file)
    writer.writerow(["国家"] + dbPageFields_Baike)
    # loop security
    if(end > len(dbcountries)):
        end = len(dbcountries)
    # loop countries
    count = 0
    for i in range(start, end):
        country = dbcountries[i]
        countryMap = countryExtractor(country)
        data2csv(writer, country, countryMap)

        print(count, " ", country, "▲")
        count += 1
    # file closed
    file.close()


def main():
    mainFiltered(0, 100)


main()
