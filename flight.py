import csv
import time

import requests
import json
import datetime
from datetime import timedelta
from fake_useragent import UserAgent


def gen_dates(start_date, day_counts):
    next_day = timedelta(days=1)  # timedalte 是datetime中的一个对象，该对象表示两个时间的差值,day=1表示相差一天
    for i in range(day_counts):  # 从起始时间的现在
        yield start_date + next_day * i


def get_date_list(start_date):
    """
    :param start_date: 开始时间
    :return: 开始时间未来40天后的日期列表
    """
    start = start_date

    end = start + datetime.timedelta(days=60)  # 爬取未来一个月的机票
    data = []
    for d in gen_dates(start, ((end - start).days)):
        data.append(d.strftime("%Y-%m-%d"))
    return data



cities_data = {"PKX":"北京",
               "CTU": "成都","CAN": "广州","CKG": "重庆","KWE":"贵阳","KMG":"昆明","KHN":"南昌","TNA":"济南","NKG":"南京","CGQ":"长春","CSX":"长沙",
               "DYG":"张家界","HAK":"海口","HRB":"哈尔滨","SJW":"石家庄","XMN":"厦门","SHE":"沈阳"}



if __name__ == "__main__":
    start_date = datetime.datetime.now()  # <class 'datetime.datetime'>
    date_data = get_date_list(start_date)

    for dcity in cities_data:
        dcityname=cities_data[dcity]
        for acity in cities_data:
            acityname = cities_data[acity]
            if dcity !=acity:
                for day in date_data:
                    url = "https://flights.ctrip.com/itinerary/api/12808/products/oneway/dcity-acity?date={}".format(day)
                    # 这里的url 必须写全！！！不能只写个path

                    headers = {
                        'User-Agent': '{}'.format(UserAgent().random),
                        'Referer': "https://flights.ctrip.com/itinerary/oneway/dcity-acity?date={}&recd=6&isMoreRec=false&".format(day),
                        "Content-Type": "application/json"
                    }
                    request_payload = {
                        "flightWay": "Oneway",
                        "classType": "ALL",
                        "hasChild": False,
                        "hasBaby": False,
                        "searchIndex": 1,
                        "airportParams": [
                            {"dcity": dcity,
                             "acity": acity,
                             "dcityname": dcityname,
                             "acityname": acityname,
                             "date": "{}".format(day),
                             }
                        ],
                    }
                    # post请求
                    response = requests.post(url, data=json.dumps(request_payload), headers=headers, timeout=30).text
                    #  json.dumps 将 Python 对象编码成 JSON 字符串
                    routeList = json.loads(response).get('data').get('routeList')  # 字典 get('key') 返回 value
                    # json.loads 将已编码的 JSON 字符串解码为 Python 对象
                    # 依次读取每条信息
                    if routeList is None:
                        pass
                    else:

                        for route in routeList:
                            # 判断是否有信息，有时候没有会报错
                            if len(route.get('legs')) == 1:
                                legs = route.get('legs')
                                flight = legs[0].get('flight')
                                # 提取想要的信息
                                airlineName = flight.get('airlineName')
                                flightNumber = flight.get('flightNumber')
                                #craftTypeName = flight.get('craftTypeName')

                                departureCityName = flight.get('departureAirportInfo').get('cityName')
                                #departureAirportName = flight.get('departureAirportInfo').get('airportName')
                                departureterminal = flight.get('departureAirportInfo').get('terminal').get('name')
                                departureDate = flight.get('departureDate')

                                arrivalCityName = flight.get('arrivalAirportInfo').get('cityName')
                                #arrivalAirportName = flight.get('arrivalAirportInfo').get('airportName')
                                #arrivalterminal = flight.get('arrivalAirportInfo').get('terminal').get('name')
                                arrivalDate = flight.get('arrivalDate')

                                cabins = legs[0].get('cabins')[0]
                                price = cabins.get('price').get('price')


                                with open(r"E:\python\flightprice\flightprice2.csv", "a+", encoding='utf-8-sig') as f:
                                    writer = csv.writer(f, dialect="excel")
                                    #基于文件对象构建 csv写入对象
                                    csv_write = csv.writer(f)
                                    csv_data = [airlineName, flightNumber,
                                               departureCityName,
                                               departureDate,arrivalDate,
                                               arrivalCityName,
                                               price, ]
                                    csv_write.writerow(csv_data)
                                    f.close()

                                print(airlineName, "\t",
                                      flightNumber, "\t",
                                      price, "\t",
                                      departureDate, "\t",
                                      arrivalDate, "\t",
                                      departureCityName, "\t",
                                      arrivalCityName, "\t",

                                    )
                            else:
                                pass
                    time.sleep(3)
            else:
                pass