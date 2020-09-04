import csv
from datetime import timedelta, datetime
import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json


def gen_dates(start_date, day_counts):
    next_day = timedelta(days=1)  # timedalte 是datetime中的一个对象，该对象表示两个时间的差值,day=1表示相差一天
    for i in range(day_counts):  # 从起始时间的现在
        yield start_date + next_day * i


def get_date_list(start_date):
    """
    :param start_date: 开始时间
    :return: 开始时间未来40天后的日期列表
    """
    if start_date < datetime.datetime.now():
        start = datetime.datetime.now()
    else:
        start = start_date

    end = start + datetime.timedelta(days=40)  # 爬取未来一个月的机票
    data = []
    for d in gen_dates(start, ((end - start).days)):
        data.append(d.strftime("%Y-%m-%d"))
    return data


# 得到所有地方航班及链接
def getAllFlights():
    flights = {}  # {'安庆航班': 'https://flights.ctrip.com/schedule/aqg..html', ...}
    url = 'https://flights.ctrip.com/schedule'
    headers = {
        'User-Agent': '{}'.format(UserAgent().random),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests': '1',
        'Connection': 'close'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    letter_list = soup.find(attrs={'class': 'letter_list'}).find_all('li')
    time.sleep(0.5)
    for li in letter_list:
        for a in li.find_all('a'):
            flights[a.get_text()] = url + a['href'][9:]
    return flights


# 得到一个地方航班的所有线路
def getFlightLines(url):
    flightlines = {}  # {'安庆-北京': 'http://flights.ctrip.com/schedule/aqg.bjs.html', ...｝
    urlc= 'https://flights.ctrip.com'
    headers = {
        'Referer': 'https://flights.ctrip.com/schedule/',
        'User-Agent': '{}'.format(UserAgent().random),
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    letter_list = soup.find(attrs={'id': 'ulD_Domestic'}).find_all('li')
    time.sleep(3)
    for li in letter_list:
        for a in li.find_all('a'):
            flightlines[a.get_text()] = urlc+a['href']

    return flightlines







if __name__ == "__main__":
    dictObj={}
    flights = getAllFlights()
    for flight in flights.values():
        flightline = getFlightLines(flight)
        print(flightline)
        dictObj.update(flightline)
        jsObj = json.dumps(dictObj)
    fileObject = open('flightlines.json', 'a+')
    fileObject.write(jsObj)
    fileObject.close()
