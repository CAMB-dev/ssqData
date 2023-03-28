import requests
from requests import Response
from bs4 import BeautifulSoup
import json
import csv

baseUrl = 'http://kaijiang.zhcw.com'


def getPageCount() -> int:
    resUri = baseUrl + '/zhcw/html/ssq/list.html'
    response: Response = requests.get(resUri)
    bs = BeautifulSoup(response.text, 'html.parser')
    return int(bs.find('p', {"class": "pg"}).find('strong').text)


def getAllData(pageCount: int) -> list[list]:
    # collection[data[]]
    result: list[list] = []
    for i in range(1, pageCount + 1):
        resUri = baseUrl + f'/zhcw/html/ssq/list_{str(i)}.html'
        response: Response = requests.get(resUri)
        bs = BeautifulSoup(response.text, 'html.parser')
        t = 0
        ems = bs.find_all('em')
        for k in range(int(len(ems) / 7)):
            result.append([int(x.text) for x in ems[t:t + 7]])
            t += 7
    return result


if __name__ == '__main__':
    results = getAllData(getPageCount())
    f = open('result.csv', 'w')
    c = csv.writer(f)
    c.writerows(results)
    f.close()
