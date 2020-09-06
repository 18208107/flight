import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from scrapy.http import headers


def getFlights(url):
    flight = {}
    urla='https://flights.ctrip.com'
    headers = {
        'Host': 'flights.ctrip.com',
        'User-Agent': '{}'.format(UserAgent().random),
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    flights_tr = soup.find(attrs={'id': 'flt1'}).find_all('tr')
    for tr in flights_tr:
        for a in tr.find_all('a'):
            flight[a.get_text()] = urla + a['href']
    return flight

def getFlightInfo(url):
    response = requests.get(url, headers=headers)
    routeList = json.loads(response).get('data').get('routeList')  # 字典 get('key') 返回 value
    # json.loads 将已编码的 JSON 字符串解码为 Python 对象
    # 依次读取每条信息
    for route in routeList:
        # 判断是否有信息，有时候没有会报错
        if len(route.get('legs')) == 1:
            legs = route.get('legs')
            flight = legs[0].get('flight')
            # 提取想要的信息
            airlineName = flight.get('airlineName')
            flightNumber = flight.get('flightNumber')
            craftTypeName = flight.get('craftTypeName')

            departureCityName = flight.get('departureAirportInfo').get('cityName')
            departureAirportName = flight.get('departureAirportInfo').get('airportName')
            departureterminal = flight.get('departureAirportInfo').get('terminal').get('name')
            departureDate = flight.get('departureDate')

            arrivalCityName = flight.get('arrivalAirportInfo').get('cityName')
            arrivalAirportName = flight.get('arrivalAirportInfo').get('airportName')
            arrivalterminal = flight.get('arrivalAirportInfo').get('terminal').get('name')
            arrivalDate = flight.get('arrivalDate')

            cabins = legs[0].get('cabins')[0]
            price = cabins.get('price').get('price')


            with open(r"D:\Anaconda3\flightprice\price.csv", "a+", encoding='utf-8-sig') as f:
                writer = csv.writer(f, dialect="excel")
                # 基于文件对象构建 csv写入对象
                csv_write = csv.writer(f)
                csv_data = [airlineName, flightNumber,
                            departureCityName,
                            departureDate, arrivalDate,
                            arrivalCityName,
                            price, ]
                csv_write.writerow(csv_data)
                f.close()
            print(airlineName, "\t",
                  flightNumber, "\t",
                  price, "\t",
                  departureDate, "\t",
                  arrivalDate, "\t",
                  craftTypeName, "\t",
                  departureCityName, "\t",
                  departureAirportName, "\t",
                  departureterminal, "\t",
                  arrivalCityName, "\t",
                  arrivalAirportName, "\t",
                  arrivalterminal, )
        else:
            pass
if __name__ == "__main__":
    url='https://flights.ctrip.com/schedule/cgq.ckg.html'
    flight = getFlights(url)
    print(flight)