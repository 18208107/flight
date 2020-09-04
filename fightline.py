import requests
import time
from bs4 import BeautifulSoup
import csv
import requests
import json

from datetime import timedelta
from fake_useragent import UserAgent


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
    time.sleep(1)
    for li in letter_list:
        for a in li.find_all('a'):
            flights[a.get_text()] = url + a['href'][9:]
    return flights


# 得到一个地方航班的所有线路
def getFlightLines(url):
    flightlines = {}  # {'安庆-北京': 'http://flights.ctrip.com/schedule/aqg.bjs.html', ...｝
    headers = {
        'Referer': 'https://flights.ctrip.com/schedule/',
        'User-Agent': '{}'.format(UserAgent().random),
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    letter_list = soup.find(attrs={'id': 'ulD_Domestic'}).find_all('li')
    time.sleep(5)
    for li in letter_list:
        for a in li.find_all('a'):
            flightlines[a.get_text()] = a['href']

    return flightlines




if __name__ == "__main__":
    i=0
    flights = getAllFlights()
    for flight in flights.values():
        flightline = getFlightLines(flight)
        print(flightline)
        i=i+1